

    return render_template("players.html", players=all_players)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)