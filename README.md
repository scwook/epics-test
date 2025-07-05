# EPICS Test Code
EPICS 개발용 테스트 저장소

### EPICS Apps
- comagTest : 콤마로 분리된 숫자 데이터 파일을 읽고 waveform record로 저장하는 테스트 코드
- restTest : 
    * restApp - aSub 레코드와 CURL 라이브러리를 이용하여 http GET 요청하는 테스트 코드 
    * systemApp - system 함수를 사용하여 curl 명령으로 http GET 요청하는 테스트 코드

### pythonTest
- opiMaker.py : text update widget을 원하는 개수만큼 만드는 코드
- oriental_ard-kd_checksum.py : 오리엔탈 모터 드라이버 ARD-KD Error check 값 계산하는 코드
- cn0531.py : Analog Device 제품 CN0531 보드 Analog output 테스트용 코드 (Raspberry Pi)
- tcp_client : TCP 통신 client 테스트 코드
- tcp_server : TCP 통신 server 테스트 코드
