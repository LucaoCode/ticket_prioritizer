from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

# Lista para armazenar os tickets (simulação de banco de dados)
tickets = []
ticketsConcluidos = [{
    "id": 1,
    "description": "Ticket 1",
    "category": "tecnico",
    "impact": "Alta",
}]

# Página principal: exibe todos os tickets (Read)
@app.route("/")
def home():
    return render_template("index.html", tickets=tickets)

# Página para criar um novo ticket (Create)
@app.route("/new", methods=["GET", "POST"])
def new_ticket():
    if request.method == "POST":
        # Coleta os dados do formulário
        description = request.form.get("description")
        category = request.form.get("category")
        impact = request.form.get("impact")
          # Inicialmente, considera o ticket como novo

        # Adiciona o ticket à lista
        ticket = {
            "id": len(tickets) + 1,  # Gera um ID simples
            "description": description,
            "category": category,
            "impact": impact
        }
        tickets.append(ticket)

        # Redireciona para a página principal
        return redirect(url_for("home"))
    return render_template("new.html")

# Página para editar um ticket (Update)
@app.route("/edit/<int:ticket_id>", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    # Localiza o ticket pelo ID
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        return "Ticket não encontrado", 404

    if request.method == "POST":
        # Atualiza os dados do ticket
        ticket["description"] = request.form.get("description")
        ticket["category"] = request.form.get("category")
        ticket["impact"] = request.form.get("impact")

        # Redireciona para a página principal
        return redirect(url_for("home"))

    return render_template("edit.html", ticket=ticket)

# Endpoint para deletar um ticket (Delete)
@app.route("/delete/<int:ticket_id>")
def delete_ticket(ticket_id):
    global tickets
    # Remove o ticket pelo ID
    tickets = [t for t in tickets if t["id"] != ticket_id]
    return redirect(url_for("home"))

@app.route("/concluidos/<int:ticket_id>", methods=["GET", "POST"])
def concluido(ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticketsConcluidos.append(ticket)  # Adiciona aos concluídos
            tickets.remove(ticket)  # Remove da lista de pendentes
            break
    return render_template("concluidos.html", ticketsConcluidos=ticketsConcluidos)  

if __name__ == "__main__":
    app.run(debug=True)
