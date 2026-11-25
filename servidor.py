import json
import re
import sys
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

import painel  # com --demo, usa pasta temporária (ver painel.py)
import armazenamento
import frequencia
import jogos
import resultados

PORTA = 8000

PAGINA = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel de Projetos - Jogos Desplugados</title>
<style>
:root{--bg:#f6f7f9;--card:#fff;--txt:#14181f;--mut:#5b6573;--bd:#d9dee5;--acc:#1f4fd8;--acc2:#b4540a;--ok:#15803d;--er:#b91c1c}
@media(prefers-color-scheme:dark){:root{--bg:#12151a;--card:#1b2028;--txt:#eef1f5;--mut:#9aa5b4;--bd:#2b333f;--acc:#7da2ff;--acc2:#f0a15f;--ok:#4ade80;--er:#f87171}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);font:16px/1.5 system-ui,Arial,sans-serif}
header{padding:20px 24px;border-bottom:1px solid var(--bd)}
h1{margin:0;font-size:22px}header p{margin:2px 0 0;color:var(--mut);font-size:14px}
main{max-width:1000px;margin:0 auto;padding:20px;display:grid;gap:16px}
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.card{background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:16px}
.card h2{margin:0 0 2px;font-size:17px}.tema{color:var(--mut);font-size:13px;margin-bottom:10px}
.tag{display:inline-block;font-size:12px;border:1px solid var(--bd);border-radius:20px;padding:0 8px;margin-left:6px;color:var(--mut)}
.big{font-size:26px;font-weight:700}.row{display:flex;gap:20px;flex-wrap:wrap;margin:6px 0}
.row small{display:block;color:var(--mut);font-size:12px}
.bar{height:10px;border-radius:5px;background:var(--bd);overflow:hidden;margin:2px 0 8px}
.bar i{display:block;height:100%;background:var(--acc)}.bar i.b{background:var(--acc2)}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--bd);vertical-align:top}
th{color:var(--mut);font-weight:600}.vazio{color:var(--mut);font-size:14px}
.forms{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
form{border:1px solid var(--bd);border-radius:8px;padding:12px;display:grid;gap:8px;align-content:start}
form h3{margin:0;font-size:15px}label{font-size:13px;color:var(--mut);display:grid;gap:2px}
input,select{font:inherit;padding:6px 8px;border:1px solid var(--bd);border-radius:6px;background:var(--bg);color:var(--txt)}
button{font:inherit;font-weight:600;padding:8px;border:0;border-radius:6px;background:var(--acc);color:var(--bg);cursor:pointer}
.msg{margin:0;font-size:13px;min-height:1.2em}.msg.ok{color:var(--ok)}.msg.erro{color:var(--er)}
</style>
</head>
<body>
<header><h1>Painel de Projetos</h1><p>Jogos Interativos de Computação Desplugada &middot; <span id="att">carregando...</span></p></header>
<main>
<section class="grid" id="jogos"></section>
<section class="card"><h2>Registrar</h2><div class="forms">
<form data-url="/api/cripto"><h3>Cripto Desplugada</h3>
<label>Grupo<input name="grupo" required maxlength="60"></label>
<label>Mensagem original (sem acento)<input name="mensagem" placeholder="SEGURANCA" maxlength="60"></label>
<label>Deslocamento (1 a 25)<input name="deslocamento" type="number" min="1" max="25" value="3"></label>
<label>Mensagem cifrada informada pela dupla<input name="tentativa" required maxlength="200"></label>
<button>Registrar</button><p class="msg"></p></form>
<form data-url="/api/ordenacao"><h3>Redes de Ordenação</h3>
<label>Grupo<input name="grupo" required maxlength="60"></label>
<label>Números (2 a 20, separados por vírgula)<input name="numeros" required value="5, 2, 8, 1, 4, 7"></label>
<button>Executar e registrar</button><p class="msg"></p></form>
<form data-url="/api/arvore"><h3>Árvore de Decisão</h3>
<label>Grupo<input name="grupo" required maxlength="60"></label>
<label>Item escolhido em segredo<select name="item" id="itens"></select></label>
<button>Executar e registrar</button><p class="msg"></p></form>
<form data-url="/api/frequencia"><h3>Frequência</h3>
<label>Aluno<input name="aluno" required maxlength="60"></label>
<label>Turma<input name="turma" required maxlength="60" value="1º Ano A"></label>
<label>Data<input name="data" type="date" required></label>
<label>Situação<select name="presente"><option value="1">Presente</option><option value="0">Falta</option></select></label>
<button>Registrar</button><p class="msg"></p></form>
</div></section>
<section class="card"><h2>Frequência</h2><div id="freq"></div></section>
<section class="card"><h2>Últimos resultados</h2><div id="res" style="overflow-x:auto"></div></section>
</main>
<script>
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const stat = (n, l) => `<div><div class="big">${esc(n)}</div><small>${esc(l)}</small></div>`;
const bar = (pct, cls) => `<div class="bar"><i class="${cls||''}" style="width:${Math.min(100, pct)}%"></i></div>`;

function corpo(j) {
  const r = j.resumo;
  if (j.id === 1) return `<div class="row">${stat(r.rodadas,"rodadas")}${stat(r.decifradas,"decifradas por terceiros")}${stat(r.protegidas,"protegidas")}</div>`;
  if (j.id === 3) return `<div class="row">${stat(r.rodadas,"rodadas")}${stat(r.acertos,"acertos")}${stat(r.media_perguntas.toFixed(1),"perguntas (média)")}</div>`;
  const nomes = Object.keys(r);
  if (!nomes.length) return '<p class="vazio">Nenhuma rodada registrada.</p>';
  const max = Math.max(1, ...nomes.flatMap(n => [r[n].media_comparacoes, r[n].media_trocas]));
  return nomes.map(n => `<strong>${esc(n)}</strong>
    <small>Comparações: ${r[n].media_comparacoes.toFixed(1)}</small>${bar(r[n].media_comparacoes/max*100)}
    <small>Trocas: ${r[n].media_trocas.toFixed(1)}</small>${bar(r[n].media_trocas/max*100,'b')}`).join("");
}

async function atualizar() {
  try {
    const d = await (await fetch("/api/painel")).json();
    $("jogos").innerHTML = d.jogos.map(j => `<div class="card"><h2>${esc(j.nome)}<span class="tag">${esc(j.status)}</span></h2>
      <div class="tema">${esc(j.tema)}</div>${corpo(j)}</div>`).join("");
    const alunos = Object.entries(d.frequencia);
    $("freq").innerHTML = alunos.length
      ? alunos.map(([a, p]) => `<div><strong>${esc(a)}</strong> &middot; ${p.toFixed(1)}%${bar(p)}</div>`).join("")
      : '<p class="vazio">Nenhum registro de frequência.</p>';
    $("res").innerHTML = d.resultados.length
      ? `<table><tr><th>Jogo</th><th>Grupo</th><th>Dados</th></tr>${d.resultados.map(r =>
          `<tr><td>${esc(r.jogo)}</td><td>${esc(r.grupo)}</td><td>${esc(r.dados)}</td></tr>`).join("")}</table>`
      : '<p class="vazio">Nenhum resultado registrado.</p>';
    const sel = $("itens"); if (!sel.options.length) d.itens.forEach((n, i) => sel.add(new Option(n, i)));
    $("att").textContent = "atualizado às " + new Date().toLocaleTimeString("pt-BR");
  } catch (e) { $("att").textContent = "sem conexão com o servidor"; }
}
document.querySelector("[name=data]").value = new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10);
document.querySelectorAll("form[data-url]").forEach(f => f.addEventListener("submit", async e => {
  e.preventDefault();
  const msg = f.querySelector(".msg"); msg.className = "msg"; msg.textContent = "Enviando...";
  try {
    const r = await fetch(f.dataset.url, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(Object.fromEntries(new FormData(f)))});
    const d = await r.json();
    msg.className = "msg " + (r.ok ? "ok" : "erro");
    msg.textContent = r.ok ? d.mensagem : d.erro;
    if (r.ok) atualizar();
  } catch (err) { msg.className = "msg erro"; msg.textContent = "Falha de conexão."; }
}));
atualizar(); setInterval(atualizar, 5000);
</script>
</body>
</html>"""


def recarregar_do_disco():
    """Relê os JSON, assim o painel enxerga o que o terminal gravou."""
    resultados.resultados[:] = armazenamento.carregar("resultados")
    frequencia.registros[:] = armazenamento.carregar("frequencia")


def montar_painel():
    recarregar_do_disco()
    resumos = {
        1: painel.resumo_cripto(),
        2: painel.resumo_ordenacao(),
        3: painel.resumo_arvore(),
    }
    nomes = {j["id"]: j["nome"] for j in jogos.listar_jogos()}

    return {
        "jogos": [{**j, "resumo": resumos.get(j["id"], {})} for j in jogos.listar_jogos()],
        "itens": [i["nome"] for i in painel.ITENS],
        "frequencia": painel.resumo_frequencia(),
        "resultados": [
            {
                "jogo": nomes.get(r["jogo_id"], r["jogo_id"]),
                "grupo": r["grupo"],
                "dados": ", ".join(f"{k}: {v}" for k, v in r["dados"].items()),
            }
            for r in reversed(resultados.listar_resultados()[-10:])
        ],
    }


def inteiro(valor, nome, minimo, maximo):
    try:
        n = int(str(valor).strip())
    except ValueError:
        raise ValueError(f"'{nome}' deve ser um número inteiro.")
    if not minimo <= n <= maximo:
        raise ValueError(f"'{nome}' deve estar entre {minimo} e {maximo}.")
    return n


def texto(dados, campo, maximo=60):
    valor = str(dados.get(campo, "")).strip()
    if not valor or len(valor) > maximo:
        raise ValueError(f"'{campo}' é obrigatório (até {maximo} caracteres).")
    return valor


def registrar(rota, d):
    recarregar_do_disco()  # evita sobrescrever o que o terminal gravou

    if rota == "/api/frequencia":
        try:
            data = datetime.strptime(str(d.get("data")), "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            raise ValueError("Data inválida.")
        presente = str(d.get("presente")) == "1"
        frequencia.registrar_frequencia(texto(d, "aluno"), texto(d, "turma"), data, presente)
        return "Frequência registrada."

    grupo = texto(d, "grupo")

    if rota == "/api/cripto":
        mensagem = str(d.get("mensagem", "")).strip() or "SEGURANCA"
        if not mensagem.isascii() or len(mensagem) > 60:
            raise ValueError("A mensagem deve ter até 60 caracteres, sem acentos.")
        desloc = inteiro(d.get("deslocamento") or 3, "deslocamento", 1, 25)
        r = painel.rodar_cripto(grupo, mensagem, desloc, texto(d, "tentativa", 200))
        final = "Decifrada corretamente." if r["acertou"] else "A tentativa não corresponde."
        return f"Cifrada: {r['mensagem_cifrada']}. {final}"

    if rota == "/api/ordenacao":
        partes = [p for p in re.split(r"[,;\s]+", str(d.get("numeros", ""))) if p]
        if not 2 <= len(partes) <= 20:
            raise ValueError("Informe de 2 a 20 números.")
        numeros = [inteiro(p, "número", -9999, 9999) for p in partes]
        painel.rodar_ordenacao(grupo, numeros)
        a, b = (x["dados"] for x in resultados.resultados[-2:])
        return (f"{a['estrategia']}: {a['comparacoes']} comparações, {a['trocas']} trocas. "
                f"{b['estrategia']}: {b['comparacoes']} comparações, {b['trocas']} trocas.")

    if rota == "/api/arvore":
        r = painel.rodar_arvore(grupo, inteiro(d.get("item"), "item", 0, len(painel.ITENS) - 1))
        final = "Acertou." if r["acertou"] else "Errou."
        return f"Identificado: {r['item_identificado']} em {r['quantidade_perguntas']} perguntas. {final}"

    raise KeyError(rota)


ROTAS = {"/api/cripto", "/api/ordenacao", "/api/arvore", "/api/frequencia"}


class Handler(BaseHTTPRequestHandler):
    def responder(self, status, tipo, corpo):
        dados = corpo.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{tipo}; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.responder(200, "text/html", PAGINA)
        elif self.path == "/api/painel":
            self.responder(200, "application/json", json.dumps(montar_painel(), ensure_ascii=False))
        else:
            self.responder(404, "text/plain", "Não encontrado")

    def do_POST(self):
        if self.path not in ROTAS:
            return self.responder(404, "text/plain", "Não encontrado")

        try:
            if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                raise ValueError("Tipo de conteúdo inválido.")
            tamanho = int(self.headers.get("Content-Length", 0))
            if tamanho > 10000:
                raise ValueError("Requisição muito grande.")
            dados = json.loads(self.rfile.read(tamanho) or b"{}")
            if not isinstance(dados, dict):
                raise ValueError("Formato inválido.")
            corpo = {"ok": True, "mensagem": registrar(self.path, dados)}
            self.responder(200, "application/json", json.dumps(corpo, ensure_ascii=False))
        except ValueError as e:
            self.responder(400, "application/json", json.dumps({"erro": str(e)}, ensure_ascii=False))

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    if "--demo" in sys.argv:
        painel.rodar_demo()

    servidor = HTTPServer(("127.0.0.1", PORTA), Handler)
    url = f"http://localhost:{PORTA}"
    print(f"Painel em {url}  (Ctrl+C para parar)")

    if "--sem-navegador" not in sys.argv:
        webbrowser.open(url)  # o socket já está aberto, então a página carrega

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado.")