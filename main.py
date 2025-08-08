#!/usr/bin/env python3

import sys
import os
from datetime import datetime

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from research_agent import ResearchAgent
from evaluation_agent import EvaluationAgent
import config

class ResearchSystem:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.evaluation_agent = EvaluationAgent()
        self.max_iterations = config.MAX_ITERATIONS
        
    def run_research_loop(self, question):
        """
        리서치-평가 피드백 루프를 실행합니다.
        
        Args:
            question (str): 리서치할 질문
        
        Returns:
            dict: 최종 결과 (research_result, evaluation_history, iterations)
        """
        print(f"\n{'='*60}")
        print(f"🔍 리서치 시작: {question}")
        print(f"{'='*60}")
        
        current_research = None
        feedback = None
        evaluation_history = []
        
        for iteration in range(1, self.max_iterations + 1):
            print(f"\n📝 반복 #{iteration}")
            print("-" * 40)
            
            # 리서치 수행
            print("🤖 리서치 에이전트 작업 중...")
            current_research = self.research_agent.research(question, feedback)
            
            if "오류가 발생했습니다" in current_research:
                print(f"❌ 리서치 오류: {current_research}")
                return {
                    "success": False,
                    "error": current_research,
                    "iterations": iteration
                }
            
            # 평가 수행
            print("⚖️  평가 에이전트 작업 중...")
            evaluation = self.evaluation_agent.evaluate(question, current_research)
            evaluation_history.append({
                "iteration": iteration,
                "evaluation": evaluation,
                "research_length": len(current_research)
            })
            
            # 평가 결과 출력
            self._print_evaluation_result(evaluation)
            
            # 충분한 품질에 도달했는지 확인
            if evaluation["is_sufficient"]:
                print(f"\n✅ 목표 품질 달성! (점수: {evaluation['score']}/10)")
                break
            
            # 피드백 설정 (다음 반복을 위해)
            feedback = evaluation["feedback"]
            if evaluation["improvement_areas"]:
                feedback += "\n\n개선이 필요한 영역:\n- " + "\n- ".join(evaluation["improvement_areas"])
            
            print(f"🔄 품질 개선이 필요합니다. 다음 반복을 진행합니다...")
        
        else:
            print(f"\n⏰ 최대 반복 횟수({self.max_iterations})에 도달했습니다.")
        
        return {
            "success": True,
            "question": question,
            "final_research": current_research,
            "evaluation_history": evaluation_history,
            "total_iterations": len(evaluation_history)
        }
    
    def _print_evaluation_result(self, evaluation):
        """평가 결과를 출력합니다."""
        score = evaluation["score"]
        
        # 점수에 따른 이모지
        if score >= 9:
            score_emoji = "🌟"
        elif score >= 7:
            score_emoji = "✅"
        elif score >= 5:
            score_emoji = "⚠️"
        else:
            score_emoji = "❌"
        
        print(f"   {score_emoji} 점수: {score}/10")
        
        if evaluation["strong_points"]:
            print("   💪 강점:")
            for point in evaluation["strong_points"]:
                print(f"      • {point}")
        
        if evaluation["improvement_areas"]:
            print("   🔧 개선점:")
            for area in evaluation["improvement_areas"]:
                print(f"      • {area}")
    
    def print_final_report(self, result):
        """최종 결과 리포트를 출력합니다."""
        if not result["success"]:
            print(f"\n❌ 리서치 실패: {result['error']}")
            return
        
        print(f"\n{'='*60}")
        print("📊 최종 리서치 결과")
        print(f"{'='*60}")
        
        print(f"📝 질문: {result['question']}")
        print(f"🔄 총 반복 횟수: {result['total_iterations']}")
        
        # 점수 변화 추이
        scores = [h["evaluation"]["score"] for h in result["evaluation_history"]]
        print(f"📈 점수 변화: {' → '.join(map(str, scores))}")
        
        final_score = result["evaluation_history"][-1]["evaluation"]["score"]
        final_emoji = "🌟" if final_score >= 9 else "✅" if final_score >= 7 else "⚠️"
        print(f"{final_emoji} 최종 점수: {final_score}/10")
        
        print(f"\n📄 최종 리서치 결과:")
        print("-" * 60)
        print(result["final_research"])
        print("-" * 60)

def main():
    # API 키 확인
    if not config.OPENAI_API_KEY:
        print("❌ 오류: OPENAI_API_KEY가 설정되지 않았습니다.")
        print("   .env 파일을 생성하고 다음과 같이 설정하세요:")
        print("   OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    system = ResearchSystem()
    
    print("🚀 AI 리서치-평가 피드백 시스템")
    print(f"⚙️  모델: {config.MODEL_NAME}")
    print(f"🎯 품질 기준: {config.QUALITY_THRESHOLD}/10")
    print(f"🔄 최대 반복: {config.MAX_ITERATIONS}회")
    
    try:
        while True:
            print(f"\n{'='*60}")
            question = input("💬 리서치할 질문을 입력하세요 (종료: 'quit' 또는 'exit'): ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 시스템을 종료합니다.")
                break
            
            if not question:
                print("⚠️  질문을 입력해주세요.")
                continue
            
            # 리서치 실행
            start_time = datetime.now()
            result = system.run_research_loop(question)
            end_time = datetime.now()
            
            # 결과 출력
            system.print_final_report(result)
            
            # 실행 시간
            duration = (end_time - start_time).total_seconds()
            print(f"⏱️  소요 시간: {duration:.1f}초")
            
            print("\n" + "="*60)
            
    except KeyboardInterrupt:
        print("\n\n👋 사용자에 의해 종료되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {str(e)}")

if __name__ == "__main__":
    main()