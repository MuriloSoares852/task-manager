import pytest
import sqlite3
import os
import sys

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, get_db_connection

# Banco de dados de teste
TEST_DATABASE = 'test_tasks.db'


@pytest.fixture
def client():
    """Fixture que cria um cliente de teste isolado"""
    # Configurar app para testes
    app.config['TESTING'] = True
    app.config['DATABASE'] = TEST_DATABASE
    
    # Remover banco de teste anterior se existir
    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)
    
    # Criar tabela de teste
    conn = sqlite3.connect(TEST_DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    
    # Criar cliente de teste
    with app.test_client() as test_client:
        yield test_client
    
    # Limpar após testes
    if os.path.exists(TEST_DATABASE):
        try:
            os.remove(TEST_DATABASE)
        except PermissionError:
            pass


def test_index_page(client):
    """Testa se a página inicial carrega"""
    response = client.get('/')
    assert response.status_code == 200


def test_create_task(client):
    """Testa criação de tarefa com dados válidos"""
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


def test_create_task_without_title(client):
    """Testa criação de tarefa sem título (deve falhar)"""
    response = client.post('/api/tasks', json={
        'description': 'Tarefa sem título'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_get_tasks(client):
    """Testa listagem de todas as tarefas"""
    # Criar tarefa primeiro
    client.post('/api/tasks', json={'title': 'Teste'})
    
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_task_by_id(client):
    """Testa busca de tarefa específica por ID"""
    # Criar tarefa
    resp = client.post('/api/tasks', json={'title': 'Buscar tarefa'})
    task_id = resp.get_json()['id']

    response = client.get(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Buscar tarefa'


def test_get_nonexistent_task(client):
    """Testa busca de tarefa inexistente"""
    response = client.get('/api/tasks/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data


def test_update_task(client):
    """Testa atualização de tarefa"""
    # Criar tarefa
    resp = client.post('/api/tasks', json={'title': 'Atualizar tarefa'})
    task_id = resp.get_json()['id']

    response = client.put(f'/api/tasks/{task_id}', json={'status': 'completed'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Tarefa atualizada com sucesso'

    # Verificar se foi atualizada
    resp = client.get(f'/api/tasks/{task_id}')
    assert resp.get_json()['status'] == 'completed'


def test_update_nonexistent_task(client):
    """Testa atualização de tarefa inexistente"""
    response = client.put('/api/tasks/9999', json={'status': 'completed'})
    assert response.status_code == 404


def test_delete_task(client):
    """Testa deleção de tarefa"""
    # Criar tarefa
    resp = client.post('/api/tasks', json={'title': 'Deletar tarefa'})
    task_id = resp.get_json()['id']

    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Tarefa deletada com sucesso'

    # Verificar se não existe mais
    resp = client.get(f'/api/tasks/{task_id}')
    assert resp.status_code == 404


def test_delete_nonexistent_task(client):
    """Testa deleção de tarefa inexistente"""
    response = client.delete('/api/tasks/9999')
    assert response.status_code == 404


def test_get_tasks_by_status(client):
    """Testa filtro de tarefas por status"""
    # Criar tarefas com status diferentes
    client.post('/api/tasks', json={'title': 'Tarefa pendente', 'status': 'pending'})
    client.post('/api/tasks', json={'title': 'Tarefa concluída', 'status': 'completed'})

    response = client.get('/api/tasks/status/pending')
    assert response.status_code == 200
    data = response.get_json()
    assert all(task['status'] == 'pending' for task in data)


def test_task_with_priority(client):
    """Testa criação de tarefa com diferentes prioridades"""
    priorities = ['low', 'medium', 'high']
    
    for priority in priorities:
        response = client.post('/api/tasks', json={
            'title': f'Tarefa {priority}',
            'priority': priority
        })
        assert response.status_code == 201
        
        task_id = response.get_json()['id']
        task = client.get(f'/api/tasks/{task_id}').get_json()
        assert task['priority'] == priority