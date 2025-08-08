from openai import OpenAI
import config

class ResearchAgent:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.MODEL_NAME
    
    def research(self, question, feedback=None):
        """
        주어진 질문에 대해 리서치를 수행합니다.
        
        Args:
            question (str): 리서치할 질문
            feedback (str, optional): 이전 리서치에 대한 피드백
        
        Returns:
            str: 리서치 결과
        """
        feedback_section = ""
        if feedback:
            feedback_section = f"\n\n이전 리서치에 대한 피드백:\n{feedback}\n위 피드백을 반영하여 리서치를 개선해주세요."
        
        prompt = config.RESEARCH_PROMPT.format(
            question=question,
            feedback_section=feedback_section
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            # UTF-8 인코딩 문제 해결
            if content:
                content = content.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
            return content
            
        except Exception as e:
            return f"리서치 중 오류가 발생했습니다: {str(e)}"
    
    def get_agent_info(self):
        """에이전트 정보를 반환합니다."""
        return {
            "name": "Research Agent",
            "role": "질문에 대한 깊이 있는 리서치 수행",
            "model": self.model
        }