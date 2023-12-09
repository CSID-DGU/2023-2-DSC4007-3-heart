from flask import Flask,render_template
from flask import request, jsonify
#from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
#CORS(app)

API_KEY = os.getenv("api_key")

#chat gpt api불러오기
client = OpenAI(
    api_key = API_KEY
)

def chatcompletion(user_input):
    output = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        presence_penalty=0,
        frequency_penalty=0,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": f"{user_input}."},
            {"role": "system", "content": "3줄로 요약해주기"},
            {"role": "system", "content": "한국어로 대답하고 존댓말로 대답하기"},
            {"role": "system", "content": "노인과 관련된 답변하기"}
        ]
    )

    print(output)
    chatgpt_output = output.choices[0].message.content#gpt 답변
    print(chatgpt_output)
    return chatgpt_output 

def chat(user_input):
    chatgpt_raw_output = chatcompletion(user_input)
    return chatgpt_raw_output 

def get_response(userText):
    return chat(userText)

@app.route("/")
def index():
    return render_template("index.html")

type=""
@app.route("/get")
def get_bot_response():
    global type
    userText = request.args.get('msg')
    options = ["1.생활지원", "2.주거지원", "3.건강의료", "4.고용,일자리", "5.돌봄","6.기타"]
    questions_and_answers = [{
            "question": "노인 목욕비 지원",
            "answer": "연 50,000원(5,000원권*10매) [*10매 산출 = 분기별 3매+3분기(하절기) 1매] 입니다."
        },
        {
            "question": "체육 지원",
            "answer": "우리 도에서는 노인체육 진흥을 위해 대회 개최지원, 시설지원 사업 등을 시행하고 있습니다. 먼저, 전남어르신생활체육대축전 지원, 전국 및 도단위 생활체육 대회 지원을 하고 있으며, 그 밖에 어르신전담생활체육지도자 배치를 지원하고 있습니다. 또한, 노인건강체육시설 지원, 공공체육시설 개보수 및 지방체육시설 확충 등 시설지원사업을 추진하고 있습니다."
        },
        {
            "question": "교통비 지원",
            "answer": "군포시는 '어르신 교통비 지원' 을 위해 2023년에 조례 제정(현재 군포시조례규칙심의회 안건상정 심의대기중), 시행을 위한 접수 및 지급 시스템 구축, 홍보 등의 절차를 준비중에 있으며 예산 확보에 지장이 없는 한 2024년중 시행을 목표로 하고 있습니다."
        },
        
        {
            "question": "식사 배달 지원",
            "answer": "재가노인 식사배달 사업은 거동이 불편한 만 65세 이상 기초생활수급자 또는 차상위계층 재가노인에게 도시락 및 밑반찬을 가정에 배달해 드리는 사업입니다. (장기요양 재가서비스 대상자는 제외)"
        },
   
        {
            "question": "독거노인·장애인 응급안전안심서비스는 무엇인가요?",
            "answer": "독거노인과 장애인의 가정에 게이트웨이, 화재감지기 등을 설치하여 화재, 질병 등 응급상황 발생 시 119에 자동으로 신고하고 응급관리요원에게 알려 대상자가 응급상황에 신속하게 대처하는 지원 체계를 구축합니다."
        },
        {
            "question": "무료양로시설 신청 대상",
            "answer": "노인장기요양보험법 제15조에 따른 수급자 중 시설 급여 대상자 입니다."
            +"- 장기요양 1~2등급"
            +"- 장기요양 3~5등급자 중 불가피한 사유, 치매 등으로 등급판정위원회에서 시설급여 대상자로 판정을 받은 자"
        },
        {
            "question": "노인복지시설 신청",
            "answer": "신청서 1부, 건강진단서 1부(노인양로시설 및 노인요양시설에 입소하고자하는 경우에 한함), 입소신청사유서 및 관련 증빙서류 각 1부 입니다."
        },
        {
            "question": "요양 병원 및 요양원 관련 문의",
            "answer": "소방청 생활안전과(044-205-7666)로 연락주시기 바랍니다."
        },
        {
            "question": "노인요양시설 신청 대상",
            "answer": "노인장기요양보험법 제15조에 따른 수급자 중 시설 급여 대상자 입니다."
    +"- 장기요양 1~2등급"
    +"- 장기요양 3~5등급자 중 불가피한 사유, 치매 등으로 등급판정위원회에서 시설급여 대상자로 판정을 받은 자"
        },
    
    
        {
            "question": "틀니 지원 사업",
            "answer": "만 65세 이상 의료급여 수급권자를 대상으로 하며, 치과에서 발급받은 신청서를 관할 구청 또는 동주민센터 방문하여 제출해주시면 됩니다."
        },
        {
            "question": "무릎 인공관절수술 지원",
            "answer": "신청일 기준 만 60세 이상(1963년생 이상)으로, ①의료급여 1·2종 ②국민기초생활수급자 ③차상위계층 ④한부모가족이 기준이 됩니다. 대상질환은 건강보험급여 '인공관절치환술(슬관절)' 인정기준에 준하는 질환자입니다. 지원대상자 선정통보 전 발생한 수술비 등 비용은 지원 제외됩니다."
        },
        {
            "question": "치과임플란트 지원",
            "answer": "'의료급여 치과임플란트'는 만 65세 이상 부분 무치악 수급자가 대상이며, 신청방법은 치과 병의원에서 발급받은 치과 임플란트 등록신청서를 관할 시.군.구 또는 읍.면.동에 방문하여 제출하거나 치과 병의원에서 국민건강보험공단에 전산등록, 승인 후 임플란트 시술을 받습니다. 임플란트는 1인당 평생 2개, 부분틀니와 중복하여 혜택이 가능합니다. 임플란트의 본인부담은 입원, 외래 구분 없이 1종 수급권자는 10%, 2종 수급권자는 20%를 부담합니다."
        },
        {
            "question": "의치보철사업 지원",
            "answer": "보건소 무료의치사업 대상자로 최종 선정되는 경우 전부의치, 부분의치(지대치 포함)의 본인부담금, 스마트 틀니를 지원 받으실 수 있습니다."
        },
        {
            "question": "노인일자리 사업",
            "answer": "노인일자리사업은 공익활동(노노케어, 공공시설 봉사 등), 사회서비스형(취약계층 전문서비스 등), 시장형(식품제조 및 판매, 매장운영 등)이 있으며 공익활동은 월30시간을 일하신 어르신에게 월 27만원을 지급합니다."
        },
        {
            "question": "노인일자리 신청방법",
            "answer": "신분증 지참 후 노인일자리 사업 수행기관 6개소 또는 온라인(복지로)에서 신청하시면 됩니다."
        },
        {
            "question": "노인일자리 참여 신청 자격",
            "answer": "공익활동형은 만 65세 이상, 사회서비스형은 만 65세 이상(일부 사업 60세), 취업알선형과 시장형 사업단은 만 60세 이상으로 신청할 수 있습니다."
        },
        {
            "question": "관련 문의",
            "answer": "시청 노인장애인과 노인복지팀(055-831-2660)으로 하여 주시면 더욱 더 친절하게 답변을 드리도록 하겠습니다."
        },
        {
            "question": "노인 학대 신고",
            "answer": "어르신 학대를 알게되거나 의심되는 경우 당황하지 말고 학대행위자로 의심되는 사람의 주요정보, 어르신 학대 상황 등 학대와 관련된 정보를 즉시 노인보호전문기관(1577-1389), 수사기관(112), 보건복지부콜센터(129), 노인학대 신고앱 '나비새김(노인지킴이)'에 신고하면 됩니다. 신고자의 비밀은 보장됩니다."
        },
        {
            "question": "노인맞춤돌봄서비스",
            "answer": "안전지원, 사회참여, 생활교육, 일상생활지원 같은 직접 서비스랑 민간후원 자원 연계 서비스를 제공하며, 개인별 조사와 상담을 통해 개인별 돌봄 욕구 및 필요정도에 따라 서비스 내용, 제공시간, 제공주기 등을 맞춤형으로 결정합니다."
        },
        {
            "question": "자격 기준 및 신청방법",
            "answer": "만 65세 이상 국민기초생활수급자, 차상위계층 또는 기초연금 수급자로서 유사 중복사업 자격에 해당되지 않는 자입니다. 주민등록상 주소지의 동 주민센터 방문하여 신청할 수 있습니다."
        },
        {
            "question": "응급안전 안심서비스",
            "answer": "독거노인 응급안전안심서비스란 실제로 홀로 사는 독거노인 가정에 화재감지기, 센서 등을 설치하여 응급상황 발생 시 119에 자동으로 신고하고 응급관리요원에게 알려 대상자가 응급상황에 신속하게 대처하는 지원 체계를 구축하는 사업입니다."
        }
    
    ]
    
    
    if userText in options:
        type=userText
        return f"{userText}을 선택하셨습니다."
    elif "홍길동" in userText and "-" in userText:
        return f"신원확인 되었습니다. 궁금하신 사항을 구체적으로 말씀해주세요. "
    elif "홍길동" in userText and "-" not in userText:
        return f"잘못된 정보입니다. 다시 입력해주세요."
    elif userText in [qa["question"] for qa in questions_and_answers]:
        for qa in questions_and_answers:
            if qa["question"]==userText:
                return qa["answer"]
    else:
        return chatcompletion(userText)

if __name__ == "__main__":
    app.run(debug=True)