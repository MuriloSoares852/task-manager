from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = 'tasks.db'

def get_db_connection():
    """Cria conexão com o banco de dados SQLite"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados com a tabela de tarefas"""
    conn = get_db_connection()
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

# Inicializa o banco ao iniciar a aplicação
init_db()

@app.route('/')
def index():
    """Página inicial com listagem de tarefas"""
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """API: Retorna todas as tarefas (READ)"""
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    conn.close()
    
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'id': task['id'],
            'title': task['title'],
            'description': task['description'],
            'status': task['status'],
            'priority': task['priority'],
            'created_at': task['created_at'],
            'updated_at': task['updated_at']
        })
    
    return jsonify(tasks_list)

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """API: Retorna uma tarefa específica (READ)"""
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    if task is None:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    
    return jsonify({
        'id': task['id'],
        'title': task['title'],
        'description': task['description'],
        'status': task['status'],
        'priority': task['priority'],
        'created_at': task['created_at'],
        'updated_at': task['updated_at']
    })

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """API: Cria uma nova tarefa (CREATE)"""
    data = request.get_json()
    
    # Validação dos dados
    if not data or not data.get('title'):
        return jsonify({'error': 'Título é obrigatório'}), 400
    
    title = data.get('title')
    description = data.get('description', '')
    status = data.get('status', 'pending')
    priority = data.get('priority', 'medium')
    
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO tasks (title, description, status, priority) VALUES (?, ?, ?, ?)',
        (title, description, status, priority)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'message': 'Tarefa criada com sucesso',
        'id': task_id
    }), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """API: Atualiza uma tarefa existente (UPDATE)"""
    data = request.get_json()
    
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    
    if task is None:
        conn.close()
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    
    # Atualiza os campos fornecidos
    title = data.get('title', task['title'])
    description = data.get('description', task['description'])
    status = data.get('status', task['status'])
    priority = data.get('priority', task['priority'])
    
    conn.execute(
        '''UPDATE tasks 
           SET title = ?, description = ?, status = ?, priority = ?, updated_at = CURRENT_TIMESTAMP
           WHERE id = ?''',
        (title, description, status, priority, task_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Tarefa atualizada com sucesso'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """API: Deleta uma tarefa (DELETE)"""
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    
    if task is None:
        conn.close()
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Tarefa deletada com sucesso'})

@app.route('/api/tasks/status/<status>', methods=['GET'])
def get_tasks_by_status(status):
    """API: Retorna tarefas filtradas por status"""
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC', (status,)).fetchall()
    conn.close()
    
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'id': task['id'],
            'title': task['title'],
            'description': task['description'],
            'status': task['status'],
            'priority': task['priority'],
            'created_at': task['created_at']
        })
    
    return jsonify(tasks_list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)