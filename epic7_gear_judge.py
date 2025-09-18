def calculate_score(option, value, character_type=None):
    """
    부 옵션의 종류와 수치를 입력받아 점수를 계산하는 함수.
    특정 캐릭터에 따라 깡옵션의 점수를 다르게 계산합니다.
    """
    if option in ['공격력%', '방어력%', '생명력%', '효과적중', '효과저항']:
        return value * 1
    elif option == '속도':
        return value * 2
    elif option == '치명확률':
        return value * 1.5
    elif option == '치명피해':
        return value * 1.1
    elif option in ['깡공', '깡방', '깡생']:
        if character_type == '깡옵효율캐릭':
            return 65
        else:
            return value * 0.5
    return 0

def recommend_role(options_stats):
    """
    옵션의 개수를 기반으로 캐릭터 역할군을 추천하는 함수.
    """
    # 옵션 개수
    num_딜 = options_stats['딜']
    num_탱 = options_stats['탱']
    num_디버프 = options_stats['디버프']
    num_속도 = options_stats['속도']

    # 딜러, 탱커 옵션이 3개 이상일 때 딜탱으로 판단
    if (num_딜 >= 2 and num_탱 >= 2) or (num_딜 >= 2 and num_탱 >= 1 and num_속도 >= 1) or \
       (num_탱 >= 2 and num_딜 >= 1 and num_속도 >= 1):
        print("- **딜탱 (주로 전사)**: 공격력과 생존 관련 옵션이 균형을 이루고 있어, 공격과 탱킹을 동시에 수행하는 캐릭터에게 좋습니다. (세트: 속도, 치명 등)")
        return
        
    # 딜러 역할군 판단
    if num_딜 >= 3:
        print("- **퓨어 딜러**: 공격력, 치명타 관련 옵션의 개수가 많아 적에게 높은 피해를 입히는 역할에 유용합니다. (세트: 속도, 치명, 적중)")
        return
        
    # 기사 또는 정령사 역할군 판단
    if num_탱 >= 3:
        print("- **기사 또는 정령사**: 생명력, 방어력 옵션의 개수가 많아 아군을 보호하거나 장기전을 버티는 역할에 유리합니다. (세트: 속도, 생명, 방어, 적중)")
        return

    # 디버퍼 역할군 판단
    if num_디버프 >= 1 and num_속도 >= 1:
        print("- **디버퍼**: 효과적중 옵션과 속도 옵션이 있어, 적에게 디버프를 거는 데 유용합니다. (세트: 속도, 적중)")
        return
    
    # 딜러/탱커 역할군 판단 (2개씩 섞였을 때)
    if num_딜 >= 2 or num_탱 >= 2:
        if num_딜 >= 2:
            print("- **딜러**: 공격력, 치명타 관련 옵션이 두 개 이상 있어, 딜링 역할에 기본적으로 사용하기 좋습니다.")
        if num_탱 >= 2:
            print("- **기사/정령사**: 생명력, 방어력 관련 옵션이 두 개 이상 있어, 탱킹 역할에 기본적으로 사용하기 좋습니다.")
        return

    # 어떤 역할군에도 명확하게 속하지 않을 때
    print("- **범용/하이브리드**: 이 장비는 특정 역할군에 치우치지 않고 다양한 캐릭터가 활용할 수 있는 범용적인 장비입니다.")


def evaluate_gear():
    """
    사용자 입력을 받아 장비의 가치를 평가하고 캐릭터 유형을 추천하는 메인 함수.
    """
    trap_options = {
        '파멸': ['효과적중'], '흡혈': ['효과적중'], '수호': ['공격력%', '치명확률', '치명피해', '효과적중'],
        '격류': ['생명력%', '깡생', '효과적중', '효과저항'], '상처': ['효과저항', '효과적중', '공격력%', '깡공'],
        '분노': [], '나머지': []
    }
    options_list = ['공격력%', '방어력%', '생명력%', '효과적중', '효과저항', '속도', '치명확률', '치명피해', '깡공', '깡방', '깡생']
    
    while True:
        print("\n" + "=" * 50)
        gear_type = input("장비 등급을 입력하세요 (영웅/전설), 종료하려면 '종료'를 입력하세요: ")
        if gear_type.lower() in ['종료', 'exit']:
            print("프로그램을 종료합니다.")
            break
        if gear_type not in ['영웅', '전설']:
            print("잘못된 등급입니다. '영웅' 또는 '전설'을 입력해주세요.")
            continue
        
        set_effect = input("장비 세트 효과를 입력하세요 (파멸, 흡혈, 수호, 격류, 상처, 분노, 나머지): ")
        if set_effect not in trap_options:
            print("잘못된 세트 효과입니다.")
            continue

        num_options = 4 if gear_type == '전설' else 3
        total_score = 0
        options_stats = {'딜': 0, '탱': 0, '속도': 0, '디버프': 0}
        has_speed_over_3 = False
        is_trap_included = False
        
        character_efficiency = input("이 장비를 사용할 캐릭터가 깡옵션 효율이 좋은 캐릭터인가요? (예/아니오): ")
        
        print(f"\n{set_effect} 세트의 {gear_type} 등급 장비 부 옵션 {num_options}개를 입력하세요.")
        print("사용 가능한 옵션: 공격력%, 방어력%, 생명력%, 효과적중, 효과저항, 속도, 치명확률, 치명피해, 깡공, 깡방, 깡생")
        print("예시: 속도 4, 치명확률 5\n")

        valid_inputs = True
        for i in range(num_options):
            try:
                user_input = input(f"{i + 1}번째 옵션을 입력하세요 (예: 속도 4): ")
                parts = user_input.split()
                if len(parts) != 2:
                    print("잘못된 형식입니다. '옵션이름 수치' 형식으로 입력해주세요.")
                    valid_inputs = False
                    break
                option_name, option_value = parts[0], float(parts[1])

                if option_name not in options_list:
                    print("존재하지 않는 옵션입니다.")
                    valid_inputs = False
                    break

                if '공격력' in option_name or '치명' in option_name: options_stats['딜'] += 1
                if '생명력' in option_name or '방어력' in option_name or '깡생' in option_name or '깡방' in option_name: options_stats['탱'] += 1
                if option_name == '속도': options_stats['속도'] += 1
                if '효과적중' in option_name or '효과저항' in option_name: options_stats['디버프'] += 1
                
                if option_name == '속도' and option_value >= 3:
                    has_speed_over_3 = True
                if option_name in trap_options.get(set_effect, []):
                    is_trap_included = True

                score = calculate_score(option_name, option_value, '깡옵효율캐릭' if character_efficiency == '예' else None)
                total_score += score
            except (ValueError, IndexError):
                print("잘못된 입력입니다. 올바른 형식으로 다시 입력해주세요.")
                valid_inputs = False
                break
        
        if not valid_inputs:
            continue

        print(f"\n계산된 장비의 초기 점수는 {total_score:.2f}점 입니다.")

        if has_speed_over_3:
            print("🚀 부 옵션에 **속도 3 이상**이 포함되어 있어, 다른 옵션에 관계없이 **무조건 강화**해 볼 가치가 있는 장비입니다.")
            recommend_role(options_stats)
        elif total_score >= 20:
            if is_trap_included:
                print("⚠️ 이 장비에는 해당 세트의 효율을 떨어뜨리는 함정 옵션이 있지만, 점수가 높아 강화해 볼 만합니다.")
                recommend_role(options_stats)
            else:
                print("✨ 이 장비는 **강화할 만한 가치가 있는 장비**입니다. 잠재력이 높으니 강화를 진행해보세요.")
                recommend_role(options_stats)
        else:
            print("💧 이 장비는 **점수가 낮아 강화하기에는 아쉬운 장비**입니다. 다른 장비를 찾아보시는 것을 추천합니다.")

        print("\n---")
        print("참고: 재련 후 예상 점수별 가치")
        print("65점 ~ 69점: PVP에서 쓸 수 있는 좋은 템")
        print("70점 ~ 74점: 비틱템")
        print("75점 이상: 평생템")

# 프로그램 실행
evaluate_gear()