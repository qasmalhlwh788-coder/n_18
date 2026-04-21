#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import uuid
import json
from spam_bot import start_attack, stop_attack, stop_all_attacks, get_attacks

app = Flask(__name__)
app.secret_key = 'spam_bot_secret_key_2024'
CORS(app)

# تخزين جلسات المستخدمين
user_sessions = {}

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def api_start_attack():
    """بدء هجوم جديد"""
    data = request.json
    tool = data.get('tool')
    params = data.get('params', {})
    
    # الحصول على معرف المستخدم
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        user_id = str(uuid.uuid4())
    
    # توليد معرف هجوم فريد
    attack_id = str(uuid.uuid4())[:8]
    
    # بدء الهجوم
    result = start_attack(user_id, attack_id, tool, params)
    
    if result:
        return jsonify({
            'success': True,
            'attack_id': attack_id,
            'user_id': user_id,
            'message': f'تم بدء الهجوم على {params.get("target", tool)}'
        })
    else:
        return jsonify({'success': False, 'message': 'فشل في بدء الهجوم'})

@app.route('/api/stop', methods=['POST'])
def api_stop_attack():
    """إيقاف هجوم محدد"""
    data = request.json
    user_id = data.get('user_id')
    attack_id = data.get('attack_id')
    
    if user_id and attack_id:
        result = stop_attack(user_id, attack_id)
        return jsonify({'success': result})
    else:
        return jsonify({'success': False, 'message': 'بيانات غير مكتملة'})

@app.route('/api/stop_all', methods=['POST'])
def api_stop_all():
    """إيقاف كل الهجمات"""
    data = request.json
    user_id = data.get('user_id')
    
    if user_id:
        result = stop_all_attacks(user_id)
        return jsonify({'success': result})
    else:
        return jsonify({'success': False, 'message': 'لم يتم العثور على المستخدم'})

@app.route('/api/status', methods=['GET'])
def api_get_status():
    """الحصول على حالة الهجمات"""
    user_id = request.headers.get('X-User-ID')
    
    if user_id:
        attacks = get_attacks(user_id)
        return jsonify({'success': True, 'attacks': attacks})
    else:
        return jsonify({'success': True, 'attacks': {}})

@app.route('/api/session', methods=['GET'])
def api_get_session():
    """الحصول على جلسة جديدة"""
    user_id = str(uuid.uuid4())
    return jsonify({'user_id': user_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
