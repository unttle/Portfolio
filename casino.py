import random
import time
import os
import string
import operator

MEMBER_FILE = "casino_members.txt"

# ==========================================
# 🛠️ 한국어 금액 변환기 (새로 추가된 기능)
# ==========================================
def parse_money(text):
    """
    '5억', '3천만', '100' 등의 입력을 정수로 변환합니다.
    """
    text = text.strip().replace(" ", "") # 공백 제거
    if text.isdigit(): # 그냥 숫자만 쓴 경우
        return int(text)
    
    total = 0
    # 단위 처리 (조, 억, 만)
    units = {'조': 1000000000000, '억': 100000000, '만': 10000}
    
    try:
        for unit, value in units.items():
            if unit in text:
                parts = text.split(unit)
                num_part = parts[0]
                # '억' 앞에 숫자가 없으면 1로 간주 (예: '억'만 치면 1억)
                num = int(num_part) if num_part else 1
                total += num * value
                text = parts[1] # 남은 뒷부분 처리
        
        # 남은 숫자 (예: '5억 500' 에서 500) 더하기
        if text:
            total += int(text)
            
        return total
    except:
        return 0 # 에러나면 0원 처리

# ==========================================
# 🛠️ 디자인 & 유틸리티 (UI)
# ==========================================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def box_print(title):
    print("┌──────────────────────────────────────────┐")
    print(f"│ {title:^40} │")
    print("└──────────────────────────────────────────┘")

def hacker_loading(task_name):
    print(f"\n  [SYSTEM] {task_name}...")
    chars = string.ascii_uppercase + string.digits + "!@#$%^&*"
    bar_len = 25
    for i in range(1, 101, 4):
        random_str = "".join(random.choice(chars) for _ in range(5))
        filled = int(bar_len * i / 100)
        bar = "█" * filled + "-" * (bar_len - filled)
        print(f"\r  [{bar}] {i}% | DATA: {random_str}", end="", flush=True)
        time.sleep(0.02)
    print(" [OK]\n")
    time.sleep(0.3)

# ==========================================
# 💾 데이터베이스 관리 (DB)
# ==========================================
def load_members():
    members = {}
    if not os.path.exists(MEMBER_FILE):
        return members
    try:
        with open(MEMBER_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 5: # id,pw,wallet,max,title
                    uid, upw, uwal, umax, utit = parts
                    members[uid] = {
                        "pw": upw,
                        "wallet": int(uwal),
                        "max": int(umax),
                        "title": utit
                    }
    except: pass
    return members

def save_members(members):
    with open(MEMBER_FILE, "w", encoding="utf-8") as f:
        for uid, data in members.items():
            line = f"{uid},{data['pw']},{data['wallet']},{data['max']},{data['title']}\n"
            f.write(line)

# ==========================================
# 🏆 랭킹 시스템
# ==========================================
def show_ranking(members):
    clear()
    box_print("🏆 HALL OF FAME (TOP 5) 🏆")
    if not members:
        print("\n  [!] 등록된 회원이 없습니다.")
        time.sleep(1); return

    sorted_users = sorted(members.items(), key=lambda x: x[1]['max'], reverse=True)
    
    print("\n   [순위]   [아이디]        [최고 자산]      [칭호]")
    print("   " + "="*45)
    
    rank = 1
    for uid, data in sorted_users[:5]:
        medal = "🥇" if rank==1 else ("🥈" if rank==2 else ("🥉" if rank==3 else f"{rank}."))
        print(f"    {medal}     {uid:<10}   {data['max']:>13,}원    {data['title']}")
        rank += 1
    
    print("\n" + "="*48)
    input("  [Enter] 키를 누르면 돌아갑니다...")

# ==========================================
# 🎮 게임 콘텐츠 (1~7번)
# ==========================================
def dice_game(wallet):
    clear()
    box_print("🎲 DICE GAME CENTER")
    try:
        # ★ 수정된 부분: int(input) -> parse_money(input)
        user_input = input(f"\n  💰 잔고: {wallet:,}원 | 배팅금(예: 5억, 100만, 0:종료) > ")
        val = parse_money(user_input) 
        
        if val <= 0: return wallet # 0원이거나 잘못된 입력이면 종료/취소
        if val > wallet:
            print("  ❌ 잔고가 부족합니다!"); time.sleep(1); return wallet
            
        print(f"  💸 배팅 금액: {val:,}원을 거셨습니다.") # 확인 메시지
        time.sleep(0.5)
        
    except: return wallet

    hacker_loading("주사위 데이터 생성")
    me, com = sum(random.randint(1,6) for _ in range(3)), sum(random.randint(1,6) for _ in range(3))
    print(f"  나: {me}  VS  컴: {com}")
    
    if me > com: print("  🎉 승리! (+1배)"); wallet += val
    elif me < com: print("  💀 패배... (-1배)"); wallet -= val
    else: print("  🤝 무승부")
    
    if wallet < 100000:
        if input("\n  [!] 파산 위기! 지원금 심사(y/n)? ").lower() == 'y':
            hacker_loading("신용 정보 조회")
            if random.randint(1,100) <= 60:
                bonus = random.randint(100000, 150000)
                wallet += bonus; print(f"  [승인] {bonus:,}원 지급!")
            else: print("  [거절] 알바 권장.")
    else:
        input("\n  [Enter]..."); 
    return wallet

def slot_game(wallet):
    clear()
    box_print("🎰 SLOT MACHINE")
    try:
        user_input = input(f"\n  💰 잔고: {wallet:,}원 | 배팅금(예: 5억, 0:종료) > ")
        val = parse_money(user_input)
        
        if val <= 0: return wallet
        if val > wallet: print("  ❌ 잔고 부족"); time.sleep(1); return wallet
    except: return wallet

    wallet -= val
    hacker_loading("슬롯 알고리즘 회전")
    sym = ["🍒", "🍋", "🍇", "💎", "7️⃣"]
    s = [random.choice(sym) for _ in range(3)]
    print(f"  [ {s[0]} ] [ {s[1]} ] [ {s[2]} ]")
    
    if s[0]==s[1]==s[2]:
        m = 50 if s[0]=="7️⃣" else 10
        print(f"  🎊 JACKPOT! {m}배!"); wallet += val*m
    elif s[0]==s[1] or s[1]==s[2] or s[0]==s[2]:
        print("  ✨ 2배 당첨!"); wallet += val*2
    else: print("  💀 꽝...")
    input("\n  [Enter]..."); return wallet

def odd_even_game(wallet):
    clear()
    box_print("🖕 ODD / EVEN")
    try:
        user_input = input(f"\n  💰 잔고: {wallet:,}원 | 배팅금(예: 100만, 0:종료) > ")
        val = parse_money(user_input)
        
        if val <= 0: return wallet
        if val > wallet: print("  ❌ 잔고 부족"); time.sleep(1); return wallet
        
        pick = input("  [1.홀 / 2.짝] 선택 > ")
    except: return wallet

    ans = random.randint(1,2)
    hacker_loading("결과 분석 중")
    print(f"  정답: {'홀' if ans==1 else '짝'}")
    if (pick=='1' and ans==1) or (pick=='2' and ans==2):
        print("  🎉 정답! (+50%)"); wallet += int(val*0.5)
    else: print("  💀 땡!"); wallet -= val
    input("\n  [Enter]..."); return wallet

def up_down_game(wallet):
    clear()
    box_print("⬆️ UP & DOWN (1~1000)")
    try:
        user_input = input(f"\n  💰 잔고: {wallet:,}원 | 배팅금(예: 5억, 0:종료) > ")
        val = parse_money(user_input)
        
        if val <= 0: return wallet
        if val > wallet: print("  ❌ 잔고 부족"); time.sleep(1); return wallet
    except: return wallet

    wallet -= val
    ans = random.randint(1, 1000)
    print("\n  [START] 숫자를 맞춰보세요!")
    success = False
    for i in range(1, 11):
        try:
            g = int(input(f"  [{i}/10] 입력 > "))
            if g == ans:
                m = 100 if i==1 else (10 if i<=3 else 2)
                print(f"  🎉 정답! {m}배 잭팟!"); wallet += val*m; success=True; break
            elif g < ans: print("  UP ⬆️")
            else: print("  DOWN ⬇️")
        except: continue
    if not success: print(f"  💀 실패. 정답: {ans}")
    input("\n  [Enter]..."); return wallet

def rsp_game(wallet):
    clear()
    box_print("🖐️ ROCK PAPER SCISSORS")
    try:
        user_input = input(f"\n  💰 잔고: {wallet:,}원 | 배팅금(예: 5억, 0:종료) > ")
        val = parse_money(user_input)
        
        if val <= 0: return wallet
        if val > wallet: print("  ❌ 잔고 부족"); time.sleep(1); return wallet
        
        u = int(input("  [1.가위 2.바위 3.보] > "))
        if u not in [1,2,3]: return wallet
    except: return wallet

    wallet -= val
    c = random.randint(1,3)
    h = {1:"가위", 2:"바위", 3:"보"}
    print(f"  나: {h[u]} VS 컴: {h[c]}")
    
    if u == c: print("  🤝 무승부 (원금)"); wallet += val
    elif (u==1 and c==3) or (u==2 and c==1) or (u==3 and c==2):
        print("  🎉 승리! (2배)"); wallet += val*2
    else: print("  💀 패배...")
    input("\n  [Enter]..."); return wallet

def title_shop(wallet, title):
    clear()
    box_print("💎 VIP SHOP")
    print(f"  내 칭호: [{title}]")
    print("  1.[자산가] 1천만 | 2.[실버VIP] 4천만 | 3.[도박의신] 2억")
    c = input("\n  선택(0:종료) > ")
    if c=="1" and wallet>=10000000: 
        wallet-=10000000; title="자산가"; hacker_loading("등급 상향 조정")
    elif c=="2" and wallet>=40000000: 
        wallet-=40000000; title="실버VIP"; hacker_loading("등급 상향 조정")
    elif c=="3" and wallet>=200000000: 
        wallet-=200000000; title="도박의신"; hacker_loading("전설 데이터 동기화")
    return wallet, title

def part_time_job(wallet):
    clear()
    box_print("🧸 ALBA (GuGuDan)")
    for i in range(3):
        a, b = random.randint(2,9), random.randint(2,9)
        if int(input(f"  {a} x {b} = ? ")) != a*b:
            print("  ❌ 실수! 알바비 없음."); time.sleep(1); return wallet
    print("  💰 20만원 입금 완료!"); wallet += 200000; time.sleep(1)
    return wallet

# ==========================================
# 🎮 게임 로비 (로그인 후 진입)
# ==========================================
def game_lobby(user_id, members):
    while True:
        my_data = members[user_id]
        if my_data['wallet'] > my_data['max']:
            my_data['max'] = my_data['wallet']
        
        clear()
        print("\n")
        print("    ##############################################")
        print("    #    💰 SEONG-MIN PREMIUM CASINO SERVER 💰   #")
        print("    ##############################################")
        print(f"\n   👤 PLAYER: [{my_data['title']}] {user_id}")
        print(f"   💳 WALLET: {my_data['wallet']:,} KRW")
        print("-" * 48)
        print("   1.🎲 DICE      2.🎰 SLOT      3.🖕 ODD/EVEN")
        print("   4.⬆️ UP/DOWN   5.🖐️ RSP       6.💎 SHOP")
        print("   7.🧸 JOB       0.🚪 LOGOUT")
        print("-" * 48)

        choice = input("\n   메뉴 선택 > ")
        
        if choice == "0":
            save_members(members)
            hacker_loading("로그아웃 및 데이터 저장")
            break
        elif choice == "1": my_data['wallet'] = dice_game(my_data['wallet'])
        elif choice == "2": my_data['wallet'] = slot_game(my_data['wallet'])
        elif choice == "3": my_data['wallet'] = odd_even_game(my_data['wallet'])
        elif choice == "4": my_data['wallet'] = up_down_game(my_data['wallet'])
        elif choice == "5": my_data['wallet'] = rsp_game(my_data['wallet'])
        elif choice == "6": 
            my_data['wallet'], my_data['title'] = title_shop(my_data['wallet'], my_data['title'])
        elif choice == "7": my_data['wallet'] = part_time_job(my_data['wallet'])
        
        elif choice == "kimsungjunsibal":
            hacker_loading("ADMIN ACCESS GRANTED")
            print("   [SYSTEM] 5억 지급 & 운영자 권한 승인.")
            my_data['wallet'] += 500000000
            my_data['title'] = "운영자"
            time.sleep(1.5)

        save_members(members)

# ==========================================
# 🚀 메인 시스템 (로그인 화면)
# ==========================================
def main_system():
    members = load_members()
    
    while True:
        clear()
        print("\n  🔒 [ SEONG-MIN CASINO LOGIN ] 🔒")
        print("-" * 35)
        print("  1. 로그인 (Login)")
        print("  2. 회원가입 (Sign Up)")
        print("  3. 랭킹 보기 (Ranking)")
        print("  0. 시스템 종료")
        print("-" * 35)
        
        choice = input("  선택 > ")
        
        if choice == "1":
            uid = input("\n  ID > ")
            upw = input("  PW > ")
            
            if uid in members and members[uid]["pw"] == upw:
                hacker_loading("서버 접속 승인")
                game_lobby(uid, members)
            else:
                print("  ❌ 정보가 일치하지 않습니다.")
                time.sleep(1)

        elif choice == "2":
            uid = input("\n  생성할 ID > ")
            if uid in members:
                print("  ❌ 이미 존재하는 아이디입니다.")
                time.sleep(1); continue
            upw = input("  사용할 PW > ")
            
            members[uid] = {"pw":upw, "wallet":1000000, "max":1000000, "title":"평민"}
            save_members(members)
            hacker_loading("계정 생성 중")
            print("  ✅ 가입 완료!")
            time.sleep(1)

        elif choice == "3":
            show_ranking(members)
            
        elif choice == "0":
            print("\n  서버를 종료합니다. Good Bye.")
            break

if __name__ == "__main__":
    main_system()