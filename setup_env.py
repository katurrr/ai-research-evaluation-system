#!/usr/bin/env python3
"""
가상환경 설정 도우미 스크립트

이 스크립트는 프로젝트의 가상환경을 자동으로 설정합니다.
"""

import os
import sys
import subprocess
import platform
import shutil

def run_command(command, description):
    """명령어를 실행하고 결과를 출력합니다."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 완료")
        if result.stdout.strip():
            print(f"   출력: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 실패: {e}")
        if e.stderr:
            print(f"   오류: {e.stderr.strip()}")
        return False

def get_python_command():
    """시스템에 맞는 Python 명령어를 반환합니다."""
    system = platform.system().lower()
    
    # Windows에서는 보통 python
    if system == "windows":
        candidates = ["python", "py", "python3"]
    else:
        # Linux/Mac에서는 python3 우선
        candidates = ["python3", "python"]
    
    for cmd in candidates:
        if shutil.which(cmd):
            try:
                result = subprocess.run([cmd, "--version"], 
                                       capture_output=True, text=True, check=True)
                if "Python 3" in result.stdout:
                    return cmd
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
    
    return None

def check_python_availability():
    """Python 설치 여부와 버전을 확인합니다."""
    python_cmd = get_python_command()
    
    if not python_cmd:
        print("❌ Python이 설치되지 않았거나 경로에서 찾을 수 없습니다.")
        print("\n📥 Python 설치 방법:")
        
        system = platform.system().lower()
        if system == "windows":
            print("  Windows: https://www.python.org/downloads/ 에서 다운로드")
            print("  또는 Microsoft Store에서 Python 검색")
        elif system == "darwin":  # macOS
            print("  macOS: brew install python")
            print("  또는 https://www.python.org/downloads/ 에서 다운로드")
        else:  # Linux
            print("  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv")
            print("  CentOS/RHEL: sudo yum install python3 python3-pip")
        
        return False, None
    
    # 버전 확인
    try:
        result = subprocess.run([python_cmd, "--version"], 
                               capture_output=True, text=True, check=True)
        version_str = result.stdout.strip()
        print(f"🐍 발견된 Python: {version_str} ({python_cmd})")
        
        # 버전 파싱
        version_parts = version_str.replace("Python ", "").split(".")
        major = int(version_parts[0])
        minor = int(version_parts[1])
        
        if major < 3 or (major == 3 and minor < 8):
            print("⚠️  경고: Python 3.8 이상을 권장합니다.")
            return False, python_cmd
        
        return True, python_cmd
        
    except Exception as e:
        print(f"❌ Python 버전 확인 실패: {e}")
        return False, None

def setup_virtual_environment():
    """가상환경을 설정합니다."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(project_dir, "venv")
    
    print(f"📁 프로젝트 디렉토리: {project_dir}")
    print(f"📁 가상환경 경로: {venv_path}")
    
    # 가상환경이 이미 존재하는지 확인
    if os.path.exists(venv_path):
        print("⚠️  가상환경이 이미 존재합니다.")
        response = input("기존 가상환경을 삭제하고 새로 만드시겠습니까? (y/N): ").strip().lower()
        if response == 'y':
            print("🗑️  기존 가상환경을 삭제하는 중...")
            shutil.rmtree(venv_path)
        else:
            print("✅ 기존 가상환경을 사용합니다.")
            return venv_path
    
    # 가상환경 생성
    python_cmd = get_python_command()
    if not python_cmd:
        print("❌ Python 명령어를 찾을 수 없습니다.")
        return None
        
    if not run_command(f"{python_cmd} -m venv {venv_path}", "가상환경 생성"):
        return None
    
    return venv_path

def install_requirements(venv_path):
    """requirements.txt에서 패키지를 설치합니다."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(project_dir, "requirements.txt")
    
    if not os.path.exists(requirements_file):
        print("⚠️  requirements.txt 파일이 없습니다.")
        return False
    
    # OS에 따른 pip 경로 설정
    if platform.system() == "Windows":
        pip_path = os.path.join(venv_path, "Scripts", "pip")
    else:
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    # pip 업그레이드
    if not run_command(f'"{pip_path}" install --upgrade pip', "pip 업그레이드"):
        return False
    
    # requirements.txt 설치
    if not run_command(f'"{pip_path}" install -r "{requirements_file}"', "패키지 설치"):
        return False
    
    return True

def setup_env_file():
    """.env 파일을 설정합니다."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    env_example = os.path.join(project_dir, ".env.example")
    env_file = os.path.join(project_dir, ".env")
    
    if os.path.exists(env_file):
        print("✅ .env 파일이 이미 존재합니다.")
        return True
    
    if os.path.exists(env_example):
        shutil.copy(env_example, env_file)
        print("📋 .env.example을 .env로 복사했습니다.")
        print("⚠️  .env 파일에서 OpenAI API 키를 설정해주세요!")
        return True
    else:
        print("⚠️  .env.example 파일이 없습니다.")
        return False

def print_usage_instructions(venv_path):
    """사용법을 출력합니다."""
    print("\n" + "="*60)
    print("🎉 설정 완료!")
    print("="*60)
    
    # OS에 따른 활성화 명령어
    if platform.system() == "Windows":
        activate_cmd = f"{venv_path}\\Scripts\\activate"
    else:
        activate_cmd = f"source {venv_path}/bin/activate"
    
    print("\n📋 사용법:")
    print("1. 가상환경 활성화:")
    print(f"   {activate_cmd}")
    print("\n2. API 키 설정:")
    print("   .env 파일을 열고 OpenAI API 키를 입력하세요")
    print("\n3. 프로그램 실행:")
    python_cmd = get_python_command() or "python"
    print(f"   {python_cmd} main.py")
    print("\n4. 가상환경 비활성화 (사용 후):")
    print("   deactivate")
    
    print("\n💡 팁:")
    print("- API 키는 https://platform.openai.com/api-keys 에서 발급받을 수 있습니다")
    print("- 프로젝트 사용 전에는 항상 가상환경을 활성화하세요")

def main():
    print("🚀 AI Research-Evaluation 시스템 환경 설정")
    print("="*60)
    
    # Python 설치 및 버전 확인
    python_ok, python_cmd = check_python_availability()
    if not python_ok:
        sys.exit(1)
        
    print(f"✅ Python 확인 완료: {python_cmd}")
    
    # 가상환경 설정
    venv_path = setup_virtual_environment()
    if not venv_path:
        print("❌ 가상환경 설정에 실패했습니다.")
        sys.exit(1)
    
    # 패키지 설치
    if not install_requirements(venv_path):
        print("❌ 패키지 설치에 실패했습니다.")
        sys.exit(1)
    
    # .env 파일 설정
    setup_env_file()
    
    # 사용법 안내
    print_usage_instructions(venv_path)

if __name__ == "__main__":
    main()