#!/usr/bin/env python3
"""
使用 Cookie 下载抖音视频
"""

import sys
sys.path.insert(0, '.')

from src.core import DouyinDownloader

# 你的 Cookie
COOKIE = "enter_pc_once=1; UIFID_TEMP=5bdad390e71fd6e6e69e3cafe6018169c2447c8bc0b8484cc0f203a274f99fdb76775d15ca462e0deffb59f62784a3213a720d3b7b80c227c7b397a1ab71e9222d5177a2657e019a096d281bddeb65c1; hevc_supported=true; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; fpk1=U2FsdGVkX1+Y0xtl1CAwHG/IdgeKnPlXg+s17S6wqK01xL1VsWzfqyFAbT/BwZrfbW44h8bfJdJcwOGuyIEmxA==; fpk2=89db729cfcdc129111f017b0e7ac324a; UIFID=5bdad390e71fd6e6e69e3cafe6018169c2447c8bc0b8484cc0f203a274f99fdb44eedfae1e140faa8886c55b364b7ebf2694d8ff93cb6a26ae6bc20772bca0aac6fd388f33d385336ed7af0c2953005087aea2ed405ccfb111fc5bee2ae842e81b52ed88f643739d2015194797568eb4058b74bacf787a3b26d704d24b8a515c976ca3554b6e4a9c040849a7a873c4a1b6c4728f799b2829f5424814be09d778; s_v_web_id=verify_mmlq1z9y_s9YVxXrw_51kT_4RKm_8RXd_IoeK2ZXWzU7z; dy_swidth=1920; dy_sheight=1080; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A20%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A0%7D%22; my_rd=2; bd_ticket_guard_client_web_domain=2; passport_csrf_token=744a9975259f8aae4e731c1da110585d; passport_csrf_token_default=744a9975259f8aae4e731c1da110585d; __ac_nonce=069b12d3800553b1f461; __ac_signature=_02B4Z6wo00f01PTQm3QAAIDDeXgi.4uVchz08J.AAFSK44; strategyABtestKey=%221773219129.68%22; is_dash_user=1; record_force_login=%7B%22timestamp%22%3A1773219129545%2C%22force_login_video%22%3A1%2C%22force_login_live%22%3A0%2C%22force_login_direct_video%22%3A1%7D; douyin.com; device_web_cpu_core=20; device_web_memory_size=8; architecture=amd64; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f2735373c343c3d3c343736323234272927676c715a75776a716a666a69273f2763646976602778; bit_env=Qq3iyNT3VU4I1LW-nqNFGRGXYOWDe2Ok3na-IbYzsaWkNgCYSATKPGP_2fSM1rJRht-fp5U2erjk8QE5Lao3iK-dJ7Clmq1VeOMqrUriR21NvPSTmbSKDNeJuuN0NffvQFzsyVG6DDypsBJ9OOO47rp0NWT5EKFtuXohmz11M1HSOlQ1TsT5I-pZb5fiqltKTTUaazVi6dXbXMjiVvfg0Rv1KF2WZWOGX0w0r_UkbNTaZHfoHrPaTAg5szLeQDwM7qVuI_rnEJXSdCWAdJ4MUHvw8tuFQ0ETxnDdj6TuwKcP5o1KKNIFOW1vWSkl4Y1Vgm2vjNwKzkDCbhA5AP43IZiInF2amKVgaip-SHJ3nVpXgLlPHyK_pmhJZFO0qhJZpicb456j8vYk24kqJilrtATgj2p26-LWBO3Ke4MqUTTyNdui9ef0eQc4Y3XNW2wIa-TvenDc2j5NX6NTBfmUg2Q2rsJ2TwfSqI_u-pzY9cmE7gH0kGyp1FldI3q_gB9N; gulu_source_res=eyJwX2luIjoiMTM2MDYwZmNhNGM1MWJkZTdhZTRiYjY1Yzk1ZWNhZTRiNjI3MzcyYTk3NDlhZmY4MTBiNThiZjcwZDZlZjZjNSJ9; passport_auth_mix_state=k84tfzqe1tgc6tkua8fudm7rdl320ql9; passport_assist_user=CkGmGARW87QTvlRp07Vc3Z1vCksurhxGnQ-VsDYiPo0YFpz1pD9mTVs9FQYvJzAF7Xn1VKhGjc_lfNntuQNI7qFfGxpKCjwAAAAAAAAAAAAAUCvtwK-nQKyV5n-GLACCGKb84hUGcqie0LXTNNGNumBxRYr04GXODt5Ar82xwAOQ-1kQiOeLDhiJr9ZUIAEiAQNX26YV; n_mh=VS_Mx_vMs-MgxYxe5VOkbzVcaqg05yOWj7D9cVvmF0I; sid_guard=b0a4709b97cc6c5f2da2bab9728717e5%7C1773219915%7C5184000%7CSun%2C+10-May-2026+09%3A05%3A15+GMT; uid_tt=b682a560bad7969459567f54616d16de; uid_tt_ss=b682a560bad7969459567f54616d16de; sid_tt=b0a4709b97cc6c5f2da2bab9728717e5; sessionid=b0a4709b97cc6c5f2da2bab9728717e5; sessionid_ss=b0a4709b97cc6c5f2da2bab9728717e5; session_tlb_tag=sttt%7C1%7CsKRwm5fMbF8torq5cocX5f_________EB6xhyfwHGX173wDcjY2HBrY7gNTE445AJR7vl0ESMGE%3D; is_staff_user=false; sid_ucp_v1=1.0.0-KDNmODQ1YTIxMTVkNjQyNGM0ZDY5OGJhOTExMDFiYmIyYWM2YWI1ODIKIQic0tCX-syABRDL4MTNBhjvMSAMMPLg6KMGOAdA9AdIBBoCaGwiIGIwYTQ3MDliOTdjYzZjNWYyZGEyYmFiOTcyODcxN2U1; ssid_ucp_v1=1.0.0-KDNmODQ1YTIxMTVkNjQyNGM0ZDY5OGJhOTExMDFiYmIyYWM2YWI1ODIKIQic0tCX-syABRDL4MTNBhjvMSAMMPLg6KMGOAdA9AdIBBoCaGwiIGIwYTQ3MDliOTdjYzZjNWYyZGEyYmFiOTcyODcxN2U1; _bd_ticket_crypt_cookie=300c859254406d86190a00ad8187fa3b; __security_mc_1_s_sdk_sign_data_key_web_protect=272a19dd-4edb-97df; __security_mc_1_s_sdk_cert_key=773679f4-4d2f-8665; __security_mc_1_s_sdk_crypt_sdk=9761b346-4f1a-98ba; __security_server_data_status=1; login_time=1773219914423; publish_badge_show_info=%220%2C0%2C0%2C1773219914709%22; DiscoverFeedExposedAd=%7B%7D; IsDouyinActive=true; SelfTabRedDotControl=%5B%5D; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTFBMV1kxL1E1UHZxbjNSYTFDZ2pxMFpHU0J6bWlqOHduOUU4ZVN3VnZpS3pUZ1YvZzNGRkY4Z2tnaEFkYWY4MGh4QUtyOTJLUTRPWmxjeFRUZDZUSTA9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; ttwid=1%7CLasb3v62LWoxHsx3Xy_ECrtfshNlOaGbU5yieDHx0RY%7C1773219920%7C327361198ca8502fd67cb541cccd9fa5ca4ec492c10b11dd657d61d7525d7f43; biz_trace_id=c61c005c; bd_ticket_guard_client_data_v2=eyJyZWVfcHVibGljX2tleSI6IkJMUExXWTEvUTVQdnFuM1JhMUNnanEwWkdTQnptaWo4d245RThlU3dWdmlLelRnVi9nM0ZGRjhna2doQWRhZjgwaHhBS3I5MktRNE9abGN4VFRkNlRJMD0iLCJ0c19zaWduIjoidHMuMi5iMGIxZjljNWE1M2Q5OTI4ZGYyOWRhNzQ5NmMxY2RlMjFmNjVkNmNlYjBiNjZjYTllMDg4NjQyZDdjMzAxMGEzYzRmYmU4N2QyMzE5Y2YwNTMxODYyNGNlZGExNDkxMWNhNDA2ZGVkYmViZWRkYjJlMzBmY2U4ZDRmYTAyNTc1ZCIsInJlcV9jb250ZW50Ijoic2VjX3RzIiwicmVxX3NpZ24iOiJENVZ3ejJrSUR2WVBwbHhxdzE3WlVSSThPUW5ZYm1DN0R2SGNjSVVwOTk0PSIsInNlY190cyI6IiN0R2VQMm9BajNWV3I0K1BJakV0NGlaU2YxTy96UkJFL291L2x4UUdzbkIzVmY4MEtkMHZYZmFEamQvT2QifQ%3D%3D; odin_tt=a43334b67f1fe8dba3edeb2f024a30425487075195d15c87364adbd88e38659cd48690d14ab31e1392e3a15c3ae42420a1a4b9ee42134995b1b6f9e62f76ccce"

# 要下载的视频链接
VIDEO_URL = "https://v.douyin.com/EIC3mlcdV4Y/"

def main():
    print("=" * 60)
    print("🎬 使用 Cookie 下载抖音视频")
    print("=" * 60)
    print()

    try:
        # 创建下载器（传入 Cookie）
        downloader = DouyinDownloader(cookie=COOKIE, async_mode=False)

        print(f"📥 目标URL: {VIDEO_URL}")
        print()

        # 下载视频
        filepath = downloader.download_video_sync(VIDEO_URL)

        print()
        print("=" * 60)
        print("✅ 下载成功！")
        print("=" * 60)
        print(f"📁 文件路径: {filepath}")

        # 获取文件大小
        import os
        file_size = os.path.getsize(filepath)
        print(f"📊 文件大小: {file_size / 1024 / 1024:.2f} MB")

        return filepath

    except Exception as e:
        print()
        print("=" * 60)
        print("❌ 下载失败")
        print("=" * 60)
        print(f"错误信息: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
