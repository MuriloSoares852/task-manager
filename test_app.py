import pytest
import sqlite3
import os
from app import app, init_db, DATABASE

@pytest.fixture
def client():
    # Usa um banco de dados temporário para os testes
    test_db = 'test_tasks.db'
    app.config['DATABASE'] = test_db

    # Remove banco anterior se existir
    if os.path.exists(test_db):
        os.remove(test_db)

    # Inicializa novo banco
    global DATABASE
    DATABASE = test_db
    init_db()

    with app.test_client() as client:
        yield client

    # Limpa após os testes
    if os.path.exists(test_db):
        os.remove(test_db)


def test_create_task(client):
    response = client.post('/api/tasks', json={
        'title': 'Nova tarefa',
        'description': 'Descrição da tarefa',
        'status': 'pending',
        'priority': 'high'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['message'] == 'Tarefa criada com sucesso'


def test_get_tasks(client):
    # Cria uma tarefa antes
    client.post('/api/tasks', json={'title': 'Teste'})
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_task_by_id(client):
    # Cria tarefa
    resp = client.post('/api/tasks', json={'title': 'Buscar tarefa'})
    task_id = resp.get_json()['id']

    response = client.get(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Buscar tarefa'


def test_update_task(client):
    # Cria tarefa
    resp = client.post('/api/tasks', json={'title': 'Atualizar tarefa'})
    task_id = resp.get_json()['id']

    response = client.put(f'/api/tasks/{task_id}', json={'status': 'done'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Tarefa atualizada com sucesso'

    # Verifica se realmente atualizou
    resp = client.get(f'/api/tasks/{task_id}')
    assert resp.get_json()['status'] == 'done'


def test_delete_task(client):
    # Cria tarefa
    resp = client.post('/api/tasks', json={'title': 'Deletar tarefa'})
    task_id = resp.get_json()['id']

    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Tarefa deletada com sucesso'

    # Verifica se não existe mais
    resp = client.get(f'/api/tasks/{task_id}')
    assert resp.status_code == 404


def test_get_tasks_by_status(client):
    # Cria duas tarefas com status diferentes
    client.post('/api/tasks', json={'title': 'Tarefa pendente', 'status': 'pending'})
    client.post('/api/tasks', json={'title': 'Tarefa concluída', 'status': 'done'})

    response = client.get('/api/tasks/status/pending')
    assert response.status_code == 200
    data = response.get_json()
    assert all(task['status'] == 'pending' for task in data)