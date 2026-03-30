"""
기존 HTML에 있던 22개 과목 + 34개 연결 데이터를 DB에 삽입하는 스크립트.
python seed_data.py 로 실행.
"""
import database as db

SUBJECTS = [
    {"id":"AMTH1009","name":"미분적분학","semester":"1-1","category":"basic","credits":3,
     "concepts":["극한","미분","적분","급수","테일러 전개"],
     "description":"함수의 극한, 미분, 적분의 기본 개념과 기법을 학습한다. 이공계 전 분야의 수학적 기초가 된다."},
    {"id":"AMTH1004","name":"선형대수","semester":"1-1","category":"basic","credits":3,
     "concepts":["벡터","행렬","고유값","선형변환","내적공간"],
     "description":"벡터 공간, 행렬 연산, 고유값 분해 등을 배운다. 기계학습과 컴퓨터 그래픽스의 수학적 기반이다."},
    {"id":"CSE103","name":"객체지향프로그래밍","semester":"1-1","category":"required","credits":3,
     "concepts":["클래스","상속","다형성","캡슐화","인터페이스"],
     "description":"C++/Java를 이용한 객체지향 프로그래밍의 기본 개념을 학습한다. 모든 프로그래밍 과목의 기초가 된다."},
    {"id":"SWCON104","name":"웹/파이선프로그래밍","semester":"1-1","category":"required","credits":3,
     "concepts":["HTML/CSS","Python","스크립팅","웹기초","데이터처리"],
     "description":"Python과 웹 기초(HTML/CSS)를 배운다. Python의 데이터 처리 능력은 이후 기계학습, 데이터 분석 과목의 실습 기반이 되며, 웹 기초는 풀스택 개발의 출발점이다."},
    {"id":"AMTH1001","name":"미분방정식","semester":"1-2","category":"basic","credits":3,
     "concepts":["ODE","라플라스 변환","연립미분방정식"],
     "description":"상미분방정식의 풀이법과 라플라스 변환을 학습한다. 신호처리 및 제어 분야의 기초가 된다."},
    {"id":"CSE201","name":"이산구조","semester":"1-2","category":"elective","credits":3,
     "concepts":["논리","집합론","그래프 이론","조합론","점화식","부울대수"],
     "description":"논리, 집합, 관계, 그래프, 조합론 등 컴퓨터 과학의 수학적 기초를 다룬다."},
    {"id":"EE211","name":"확률및랜덤변수","semester":"2-1","category":"basic","credits":3,
     "concepts":["확률분포","기댓값","분산","베이즈 정리","랜덤변수"],
     "description":"확률 이론, 랜덤 변수, 주요 확률분포 및 베이즈 정리를 학습한다."},
    {"id":"CSE203","name":"컴퓨터구조","semester":"2-1","category":"required","credits":3,
     "concepts":["CPU","ISA","파이프라이닝","캐시","메모리 계층"],
     "description":"CPU 구조, 명령어 집합, 파이프라이닝, 캐시 등 컴퓨터 하드웨어의 동작 원리를 학습한다."},
    {"id":"CSE204","name":"자료구조","semester":"2-1","category":"required","credits":3,
     "concepts":["연결리스트","스택/큐","트리","그래프","해시테이블","힙"],
     "description":"데이터를 효율적으로 저장하고 관리하는 자료구조를 학습하고 직접 구현한다."},
    {"id":"EE209","name":"논리회로","semester":"2-1","category":"required","credits":3,
     "concepts":["논리게이트","부울대수","플립플롭","조합회로","순서회로"],
     "description":"디지털 논리 게이트, 조합/순서 회로 설계를 학습한다. 컴퓨터 하드웨어의 기초이다."},
    {"id":"SWCON201","name":"오픈소스SW개발","semester":"2-2","category":"required","credits":3,
     "concepts":["Git","Linux","오픈소스","협업도구","코드리뷰"],
     "description":"Git 버전 관리, Linux 명령어, 오픈소스 프로젝트 참여 방법을 학습한다. 이후 소프트웨어공학, 캡스톤디자인 등 팀 프로젝트 과목에서 필수적으로 활용되는 협업 기술의 기반이다."},
    {"id":"SWCON253","name":"기계학습","semester":"2-2","category":"required","credits":3,
     "concepts":["회귀","분류","SVM","결정트리","교차검증","특성공학"],
     "description":"지도/비지도 학습의 기본 알고리즘과 모델 평가 방법을 학습한다."},
    {"id":"CSE301","name":"운영체제","semester":"3-1","category":"required","credits":3,
     "concepts":["프로세스","스레드","가상메모리","동기화","스케줄링","교착상태"],
     "description":"프로세스 관리, 메모리 관리, 파일 시스템 등 운영체제의 핵심 개념을 학습한다."},
    {"id":"CSE302","name":"컴퓨터네트워크","semester":"3-1","category":"required","credits":3,
     "concepts":["TCP/IP","HTTP","라우팅","소켓","DNS","혼잡제어"],
     "description":"OSI/TCP-IP 모델, 프로토콜, 라우팅, 소켓 프로그래밍 등 네트워크 통신 원리를 학습한다."},
    {"id":"CSE304","name":"알고리즘","semester":"3-1","category":"required","credits":3,
     "concepts":["DP","분할정복","그래프탐색","최단경로","NP","그리디"],
     "description":"정렬, 탐색, DP, 그래프 알고리즘 등 문제 해결 전략과 복잡도 분석을 학습한다."},
    {"id":"CSE305","name":"데이터베이스","semester":"3-1","category":"required","credits":3,
     "concepts":["SQL","정규화","트랜잭션","인덱스","ER모델","동시성제어"],
     "description":"관계형 데이터베이스의 설계, SQL, 트랜잭션 관리 등을 학습한다."},
    {"id":"CSE327","name":"소프트웨어공학","semester":"3-2","category":"required","credits":3,
     "concepts":["Agile","UML","디자인패턴","테스팅","SOLID"],
     "description":"소프트웨어 개발 방법론, 설계 패턴, 테스팅, 프로젝트 관리를 학습한다."},
    {"id":"CSE322","name":"컴파일러","semester":"3-2","category":"elective","credits":3,
     "concepts":["렉싱","파싱","AST","코드생성","최적화"],
     "description":"어휘/구문/의미 분석, 중간 코드 생성, 최적화 등 컴파일러의 전 과정을 학습한다."},
    {"id":"CSE331","name":"딥러닝","semester":"3-2","category":"elective","credits":3,
     "concepts":["CNN","RNN","Transformer","역전파","최적화"],
     "description":"심층 신경망의 구조와 학습 방법을 학습한다. 기계학습의 심화 과목이다."},
    {"id":"CSE423","name":"정보보호","semester":"4-1","category":"elective","credits":3,
     "concepts":["암호학","TLS","접근제어","웹보안","해시함수"],
     "description":"암호학, 네트워크/시스템/웹 보안의 기본 원리와 방어 기법을 학습한다."},
    {"id":"CSE405","name":"졸업프로젝트","semester":"4-1","category":"required","credits":3,
     "concepts":["연구","프로토타입","논문작성","시스템설계"],
     "description":"4학년 졸업 연구/개발 프로젝트를 수행하고 결과물을 발표한다. 3학년까지 배운 알고리즘, 소프트웨어공학, 전공 심화 과목의 지식을 종합적으로 적용하는 과목이다."},
    {"id":"CSE406","name":"캡스톤디자인","semester":"4-1","category":"required","credits":3,
     "concepts":["팀프로젝트","시스템통합","발표","PM"],
     "description":"팀 기반 종합 설계 프로젝트를 통해 실무 역량을 배양한다."},
]

CONNECTIONS = [
    {"from_id":"AMTH1004","to_id":"SWCON253","type":"prereq","reason":"기계학습의 핵심 연산인 행렬 곱셈, 고유값 분해, SVD 등이 모두 선형대수에서 다루는 개념이다.","shared":["행렬","고유값","선형변환"]},
    {"from_id":"AMTH1004","to_id":"CSE331","type":"prereq","reason":"딥러닝의 가중치 행렬 연산, 역전파의 야코비안 행렬 등은 선형대수 없이 이해할 수 없다.","shared":["행렬","벡터"]},
    {"from_id":"EE211","to_id":"SWCON253","type":"prereq","reason":"베이즈 분류기, 확률적 모델, 우도 함수 등 ML 알고리즘의 수학적 기반이 확률론이다.","shared":["확률분포","베이즈 정리","기댓값"]},
    {"from_id":"AMTH1009","to_id":"AMTH1001","type":"prereq","reason":"미분방정식을 풀려면 미분과 적분의 기본 기법을 반드시 알아야 한다.","shared":["미분","적분"]},
    {"from_id":"AMTH1009","to_id":"SWCON253","type":"prereq","reason":"경사하강법의 편미분, 손실함수의 최적화 등 ML의 핵심이 미적분에 기초한다.","shared":["미분","적분"]},
    {"from_id":"CSE103","to_id":"CSE204","type":"prereq","reason":"자료구조를 클래스로 구현하려면 OOP 문법(클래스, 상속, 포인터 개념)이 필수다.","shared":["클래스","상속"]},
    {"from_id":"CSE201","to_id":"CSE204","type":"prereq","reason":"트리, 그래프 자료구조는 이산구조의 그래프 이론에서 직접 파생된다.","shared":["그래프 이론","집합론"]},
    {"from_id":"CSE201","to_id":"CSE304","type":"prereq","reason":"알고리즘의 시간복잡도 분석에 점화식을 쓰고, 그래프 알고리즘은 그래프 이론이 기반이다.","shared":["그래프 이론","점화식","조합론"]},
    {"from_id":"CSE201","to_id":"EE209","type":"prereq","reason":"논리회로의 부울대수와 논리식 간소화는 이산구조에서 배운 논리와 부울대수 그 자체다.","shared":["부울대수","논리"]},
    {"from_id":"CSE204","to_id":"CSE304","type":"prereq","reason":"알고리즘은 자료구조 위에서 동작한다. 그래프 탐색은 그래프를, 우선순위 큐 문제는 힙을 사용한다.","shared":["트리","그래프","힙"]},
    {"from_id":"EE209","to_id":"CSE203","type":"prereq","reason":"CPU의 ALU는 가산기의 확장이고, 레지스터는 플립플롭으로 구성된다.","shared":["논리게이트","플립플롭","조합회로"]},
    {"from_id":"CSE203","to_id":"CSE301","type":"prereq","reason":"OS의 인터럽트 처리, 캐시 관리, 가상메모리 모두 컴퓨터 구조 지식이 필수다.","shared":["캐시","메모리 계층"]},
    {"from_id":"SWCON253","to_id":"CSE331","type":"extends","reason":"딥러닝은 기계학습의 신경망 파트를 심화 확장한 것이다. 손실함수, 경사하강법 등 ML 기초가 전제된다.","shared":["분류","회귀","교차검증"]},
    {"from_id":"CSE103","to_id":"CSE327","type":"prereq","reason":"GoF 디자인 패턴과 SOLID 원칙은 OOP 개념(상속, 다형성, 인터페이스) 위에서만 의미가 있다.","shared":["상속","다형성","인터페이스"]},
    {"from_id":"CSE204","to_id":"CSE322","type":"prereq","reason":"컴파일러는 AST(트리), 심볼테이블(해시), 파싱 스택 등 자료구조를 핵심적으로 사용한다.","shared":["트리","해시테이블","스택/큐"]},
    {"from_id":"CSE204","to_id":"CSE301","type":"prereq","reason":"OS의 스케줄링 큐, 페이지 테이블, 파일시스템 트리 등이 자료구조를 직접 활용한다.","shared":["스택/큐","트리","해시테이블"]},
    {"from_id":"CSE204","to_id":"CSE305","type":"overlap","reason":"DB 인덱스는 B-트리/B+트리로 구현되며, 해시 인덱스는 해시테이블 개념 그대로다.","shared":["트리","해시테이블"]},
    {"from_id":"CSE301","to_id":"CSE305","type":"overlap","reason":"DB의 트랜잭션 동시성 제어(락, 교착상태)는 OS 동기화 개념과 동일한 문제다.","shared":["동기화","교착상태"]},
    {"from_id":"CSE304","to_id":"CSE302","type":"overlap","reason":"네트워크 라우팅(다익스트라, 벨만-포드)은 알고리즘에서 배운 최단경로 알고리즘 그대로다.","shared":["최단경로","그래프탐색"]},
    {"from_id":"CSE304","to_id":"CSE322","type":"overlap","reason":"컴파일러 최적화에 DP와 그래프 알고리즘(데이터 흐름 분석)이 사용된다.","shared":["DP","그래프탐색"]},
    {"from_id":"CSE201","to_id":"CSE305","type":"overlap","reason":"관계형 DB의 '관계'는 이산구조의 관계 개념에서 유래했으며, SQL의 집합 연산은 집합론에 기초한다.","shared":["집합론","논리"]},
    {"from_id":"CSE302","to_id":"CSE423","type":"overlap","reason":"TLS/SSL, 방화벽, 패킷 분석 등 네트워크 보안은 프로토콜 스택 이해를 요구한다.","shared":["TCP/IP","HTTP"]},
    {"from_id":"CSE327","to_id":"CSE406","type":"prereq","reason":"캡스톤디자인에서 팀 프로젝트를 수행하려면 소프트웨어 개발 방법론과 설계 원칙이 필수다.","shared":["Agile","디자인패턴","테스팅"]},
    {"from_id":"SWCON104","to_id":"SWCON253","type":"prereq","reason":"기계학습 실습에서 Python으로 데이터 전처리, 모델 구현, 시각화를 수행하므로 Python 프로그래밍 능력이 필수다.","shared":["Python","스크립팅"]},
    {"from_id":"SWCON104","to_id":"CSE305","type":"overlap","reason":"웹 백엔드에서 DB를 연동하는 기본 구조를 이해하는 데 웹 기초 지식이 도움이 된다.","shared":["웹기초"]},
    {"from_id":"CSE103","to_id":"SWCON201","type":"prereq","reason":"오픈소스 프로젝트 참여와 Git 협업에는 OOP 기반의 코드 작성 능력이 기본 전제가 된다.","shared":["클래스"]},
    {"from_id":"SWCON201","to_id":"CSE327","type":"prereq","reason":"소프트웨어공학에서 다루는 버전 관리, 코드 리뷰, CI/CD 개념은 Git과 오픈소스 도구 경험이 기반이다.","shared":["Git","협업도구"]},
    {"from_id":"SWCON201","to_id":"CSE406","type":"prereq","reason":"캡스톤디자인의 팀 협업에서 Git 브랜칭 전략과 오픈소스 개발 프로세스를 실전에서 활용한다.","shared":["Git","협업도구"]},
    {"from_id":"CSE304","to_id":"CSE405","type":"prereq","reason":"졸업프로젝트에서 문제를 정의하고 효율적인 해법을 설계하려면 알고리즘적 사고가 필수다.","shared":["DP","그래프탐색"]},
    {"from_id":"CSE327","to_id":"CSE405","type":"prereq","reason":"졸업프로젝트의 체계적 수행을 위해 요구사항 분석, 설계, 테스팅 등 소프트웨어공학 방법론이 필요하다.","shared":["Agile","테스팅"]},
    {"from_id":"CSE301","to_id":"CSE302","type":"overlap","reason":"소켓 프로그래밍은 OS의 프로세스/스레드 모델 위에서 동작하며, 동시 접속 처리에 동기화 개념이 사용된다.","shared":["프로세스","스레드","동기화"]},
    {"from_id":"CSE201","to_id":"CSE322","type":"prereq","reason":"컴파일러의 렉서는 유한 오토마타(DFA)로 동작하고, 파서는 문맥 자유 문법에 기반한다. 이산구조의 논리와 형식 언어가 직접적 기초다.","shared":["논리","조합론"]},
    {"from_id":"EE211","to_id":"CSE302","type":"overlap","reason":"네트워크의 혼잡제어와 큐잉 이론은 확률 모델과 랜덤 프로세스 개념을 활용한다.","shared":["확률분포","랜덤변수"]},
    {"from_id":"CSE305","to_id":"CSE423","type":"overlap","reason":"SQL Injection 방어와 DB 접근제어는 데이터베이스와 보안의 직접적 교차 영역이다.","shared":["SQL","접근제어"]},
]


def seed():
    db.init_db()
    if not db.is_db_empty():
        print("DB already has data. Skipping seed.")
        return

    print(f"Inserting {len(SUBJECTS)} subjects...")
    for s in SUBJECTS:
        db.create_subject(s)

    print(f"Inserting {len(CONNECTIONS)} connections...")
    for c in CONNECTIONS:
        db.create_connection(c)

    print("Seed complete!")


if __name__ == "__main__":
    seed()
