"""Testes de Integração para a API de Jogos."""


def test_criar_jogo(client, categoria):
    resposta = client.post(
        "/api/jogos",
        json={
            "titulo": "Chrono Trigger",
            "datapublicao": "11-03-1995",
            "desenvolvedor": "Square",
            "distribuidora": "Square",
            "estoque": 15,
            "categoria_id": categoria["id"],
        },
    )
    assert resposta.status_code == 201
    dados = resposta.get_json()
    assert dados["titulo"] == "Chrono Trigger"
    assert dados["estoque"] == 15


def test_estoque_ausente_assume_zero(client, categoria):
    resposta = client.post(
        "/api/jogos",
        json={
            "titulo": "Final Fantasy VII",
            "datapublicao": "31-01-1997",
            "desenvolvedor": "Square",
            "distribuidora": "Sony",
            "categoria_id": categoria["id"],
        },
    )
    assert resposta.status_code == 201
    assert resposta.get_json()["estoque"] == 0


def test_data_publicacao_futura_devolve_422(client, categoria):
    resposta = client.post(
        "/api/jogos",
        json={
            "titulo": "Game do Futuro",
            "datapublicao": "01-01-2099",
            "desenvolvedor": "Indie",
            "distribuidora": "Indie",
            "categoria_id": categoria["id"],
        },
    )
    assert resposta.status_code == 422
    assert "datapublicao" in resposta.get_json()["erros"]


def test_categoria_inexistente_devolve_422(client):
    resposta = client.post(
        "/api/jogos",
        json={
            "titulo": "Jogo Orfao",
            "datapublicao": "10-10-2020",
            "desenvolvedor": "Dev",
            "distribuidora": "Pub",
            "categoria_id": 999,
        },
    )
    assert resposta.status_code == 422
    assert "categoria_id" in resposta.get_json()["erros"]


def test_filtro_por_categoria(client, jogo, categoria):
    outra_categoria = client.post(
        "/api/categorias", json={"nome": "Ação", "descricao": "Jogos de ação"}
    ).get_json()

    client.post(
        "/api/jogos",
        json={
            "titulo": "Devil May Cry 5",
            "datapublicao": "08-03-2019",
            "desenvolvedor": "Capcom",
            "distribuidora": "Capcom",
            "categoria_id": outra_categoria["id"],
        },
    )

    assert len(client.get("/api/jogos").get_json()) == 2

    filtrados = client.get(f"/api/jogos?categoria_id={categoria['id']}").get_json()
    assert len(filtrados) == 1
    assert filtrados[0]["titulo"] == jogo["titulo"]


def test_patch_preserva_os_campos_nao_enviados(client, jogo):
    resposta = client.patch(
        f"/api/jogos/{jogo['id']}",
        json={"estoque": 50}
    )
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["estoque"] == 50
    assert corpo["titulo"] == jogo["titulo"]
    assert corpo["desenvolvedor"] == jogo["desenvolvedor"]


def test_put_sem_estoque_zera_o_estoque(client, jogo):
    """Substituição completa (PUT): campos omitidos com default retornam ao padrão."""
    resposta = client.put(
        f"/api/jogos/{jogo['id']}",
        json={
            "titulo": jogo["titulo"],
            "datapublicao": "25-02-2022",
            "desenvolvedor": jogo["desenvolvedor"],
            "distribuidora": jogo["distribuidora"],
            "categoria_id": jogo["categoria_id"],
        },
    )
    assert resposta.status_code == 200
    assert resposta.get_json()["estoque"] == 0


def test_mover_para_categoria_inexistente_nao_altera_o_jogo(client, jogo):
    resposta = client.patch(
        f"/api/jogos/{jogo['id']}",
        json={"categoria_id": 999}
    )
    assert resposta.status_code == 422

    # Garante atomidade: o jogo permanece inalterado no banco
    atual = client.get(f"/api/jogos/{jogo['id']}").get_json()
    assert atual["categoria_id"] == jogo["categoria_id"]


def test_delete_jogo(client, jogo):
    assert client.delete(f"/api/jogos/{jogo['id']}").status_code == 204
    assert client.get(f"/api/jogos/{jogo['id']}").status_code == 404


def test_metodo_nao_permitido_devolve_json(client):
    resposta = client.patch("/api/jogos")
    assert resposta.status_code == 405
    assert resposta.get_json()["code"] == 405