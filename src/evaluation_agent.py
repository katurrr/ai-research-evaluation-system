from openai import OpenAI
import json
import config

class EvaluationAgent:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.MODEL_NAME
        self.threshold = config.QUALITY_THRESHOLD
    
    def evaluate(self, question, research_result):
        """
        리서치 결과의 품질을 평가합니다.
        
        Args:
            question (str): 원본 질문
            research_result (str): 평가할 리서치 결과
        
        Returns:
            dict: 평가 결과 (score, is_sufficient, feedback, strong_points, improvement_areas)
        """
        prompt = config.EVALUATION_PROMPT.format(
            question=question,
            research_result=research_result
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            evaluation_text = response.choices[0].message.content
            # UTF-8 인코딩 문제 해결
            if evaluation_text:
                evaluation_text = evaluation_text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
            
            # JSON 파싱 시도
            try:
                evaluation = json.loads(evaluation_text)
                
                # is_sufficient 값이 없으면 점수를 기준으로 설정
                if "is_sufficient" not in evaluation:
                    evaluation["is_sufficient"] = evaluation.get("score", 0) >= self.threshold
                
                # 필수 필드 확인 및 기본값 설정
                evaluation.setdefault("score", 0)
                evaluation.setdefault("feedback", "평가를 완료했습니다.")
                evaluation.setdefault("strong_points", [])
                evaluation.setdefault("improvement_areas", [])
                
                return evaluation
                
            except json.JSONDecodeError:
                # JSON 파싱 실패 시 텍스트에서 점수 추출 시도
                score = self._extract_score_from_text(evaluation_text)
                return {
                    "score": score,
                    "is_sufficient": score >= self.threshold,
                    "feedback": evaluation_text,
                    "strong_points": [],
                    "improvement_areas": []
                }
                
        except Exception as e:
            return {
                "score": 0,
                "is_sufficient": False,
                "feedback": f"평가 중 오류가 발생했습니다: {str(e)}",
                "strong_points": [],
                "improvement_areas": []
            }
    
    def _extract_score_from_text(self, text):
        """텍스트에서 점수를 추출합니다."""
        import re
        
        # 점수 패턴 찾기 (예: "점수: 7", "score: 8", "7점" 등)
        patterns = [
            r'점수[:\s]*(\d+)',
            r'score[:\s]*(\d+)',
            r'(\d+)점',
            r'(\d+)/10'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue
        
        return 5  # 기본 점수
    
    def get_agent_info(self):
        """에이전트 정보를 반환합니다."""
        return {
            "name": "Evaluation Agent",
            "role": "리서치 결과의 품질 평가 및 피드백 제공",
            "model": self.model,
            "threshold": self.threshold
        }