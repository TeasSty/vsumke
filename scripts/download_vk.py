# -*- coding: utf-8 -*-
"""Download VK photos at max resolution into assets/."""
from __future__ import annotations

import os
import re
import shutil
import urllib.request

OUT = r"C:\Users\popoo\Desktop\в сумке\assets"
os.makedirs(OUT, exist_ok=True)

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def upgrade_url(url: str) -> str:
    if "as=" not in url:
        return url
    m = re.search(r"as=([^&]+)", url)
    if not m:
        return re.sub(r"cs=\d+x\d+", "cs=0x0", url)
    best = None
    best_area = -1
    for s in m.group(1).split(","):
        try:
            w, h = s.lower().split("x")
            area = int(w) * int(h)
            if area > best_area:
                best_area = area
                best = s
        except ValueError:
            continue
    if best:
        if re.search(r"cs=\d+x\d+", url):
            url = re.sub(r"cs=\d+x\d+", f"cs={best}", url)
        else:
            url = url + f"&cs={best}"
    return url


def download(url: str, name: str) -> bool:
    path = os.path.join(OUT, name)
    full = upgrade_url(url)
    req = urllib.request.Request(
        full, headers={"User-Agent": UA, "Referer": "https://vk.ru/"}
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
        print(f"OK  {name:28s} {len(data):8d} B")
        return True
    except Exception as e:
        print(f"FAIL {name}: {e}")
        return False


# All unique wall photos from https://vk.ru/lnbag (cs will be upgraded)
RAW = [
    "https://sun9-25.vkuserphoto.ru/s/v1/ig2/Ms2tSYQRi_6iOrAZcKOjSkB28GZAHuZ7Kn15v5bpLNvZnKaM80M_ooc13rd7oP19dGPED2IcQh-Kj5ihWEpxemcY.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1280x1707,1440x1920,1920x2560&from=bu&u=IwAyPREBtCZlpleUorp6aMoDoYdEzp_-UoxgDK3glfg&cs=640x0",
    "https://sun9-30.vkuserphoto.ru/s/v1/ig2/Cg_yA6O1_KjPit4j22JT-ViIQNR9i1UKdyPi1mPBw5swvc0pz8fACxUlLATcRw-Q0MamPzJMaR2BaXSV8YyLlLzx.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1280x1707,1440x1920,1920x2560&from=bu&u=GyUc6U8bOCRvA38Qq4uL_BVawM8rzzV3GSSa14jonRo&cs=640x0",
    "https://sun9-78.vkuserphoto.ru/s/v1/ig2/1HtW19WnhdxHurjOAJHB3g9rJ5-KveTHqC_8ViTGamW93aFcihjyDj3_fS46xnzcVKFoN2Yb89sNlL6UjP3RJPMn.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1280x1707,1440x1920,1920x2560&from=bu&u=lZK5Xg14zz5EL0NQxJXNYLwNw1VWgghanuVb4BVSHIQ&cs=640x0",
    "https://sun9-44.vkuserphoto.ru/s/v1/ig2/5fqf3hC_8g24uMCpaTcECboVz7R7avhh4glddn0e-kQvZQzkF3umif5-VPbhPQiezkOkO68PFl7FVKIhO1HnCtw4.jpg?quality=95&as=32x45,48x68,72x101,108x152,160x226,240x338,360x507,480x677,540x761,640x902,720x1015,1080x1522,1280x1804,1440x2030,1816x2560&from=bu&u=3TcQjCn7j-vJYGv4wfDuAxEnudZW9JGfpIuFnZ9Nu5o&cs=540x0",
    "https://sun9-81.vkuserphoto.ru/s/v1/ig2/567pfgD9L1NAuyQAV5dAXTkRZhB4bI3HQcQRtcSlkXTlNuBm5YlYlQBuJx4z04s9Aj_wIgLYGZjBFlYT3TYf_HlJ.jpg?quality=95&as=32x38,48x57,72x86,108x129,160x191,240x287,360x431,480x574,540x646,640x766,720x861,1080x1292,1280x1531,1320x1579&from=bu&u=uFlQ_jM2ikEscEeKdYR-Qb6tAx4QpQn0xvg4T8MnyWY&cs=540x0",
    "https://sun9-82.vkuserphoto.ru/s/v1/ig2/qdMZg69CrxL-4wwO3afu_JXBi0h5_Ix-PMAcij1Vh3rlc8Vl08pYFIC0bjEIh-SPZ5afkzGsT-FxkZjwEgHF62TS.jpg?quality=95&as=32x52,48x78,72x116,108x175,160x259,240x388,360x582,480x777,540x874,640x1036,720x1165&from=bu&u=G0PQbh4os7fPMPntSHa-nJt4eN11PyGDXzRJ4AL4Dxw&cs=360x0",
    "https://sun9-75.vkuserphoto.ru/s/v1/ig2/oEWpYWej-o-pbHrsZUWYyMUY0S_hUdu5uMg78HXCWZX5N3mnw5XalzGPzeE_Fsfa7hSgIGocT64hjZzIeJFzd_gB.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1280x1707,1440x1920,1920x2560&from=bu&u=au6xG_PIeYkj8UiCG1jn7rM1V2fkEb_z-ZZzG7LCXSc&cs=540x0",
    "https://sun9-45.vkuserphoto.ru/s/v1/ig2/lbV-Y2IyKt0ShBjiwdKLVdNXwyHpQBMVwFcX0jW5jCSus-1DvBPtcbCvyQyYPgTZHqCCbz0wGWI_JESY2kHJLoaH.jpg?quality=95&as=32x57,48x85,72x128,108x192,160x284,240x427,360x640,480x853,540x960,640x1138,720x1280,1080x1920,1215x2160&from=bu&u=gtwRhT-0HgOFM53OjKFlxYs13nQ2_cvqR9bcxgU5Xo4&cs=360x0",
    "https://sun9-62.vkuserphoto.ru/s/v1/ig2/2d1S8NhvJ7uzGSF_3fnLhyV693f-OQyer1HMnWBvVw4rOl4mGvfGinwr_TCf1FKSa4QKL5cOaJ-fcdYv1aJsjPzd.jpg?quality=95&as=32x34,48x52,72x77,108x116,160x172,240x258,360x387,480x516,540x581,640x688,720x774,1080x1162,1280x1377,1440x1549,2380x2560&from=bu&u=k3idg37Co0wfaxw2r1x1qszGU9oMXFWnWyGn7IaITXo&cs=540x0",
    "https://sun9-75.vkuserphoto.ru/s/v1/ig2/ey0wgXt0k80F3S1_wRKyvlziDSygWKi-sbeojCITcPiZIOQk9ElTVfdEXM40aJM9-RhSy3BCdDm_ud2Nt1542mfz.jpg?quality=95&as=32x48,48x72,72x108,108x162,160x240,240x360,360x540,480x720,540x810,640x960,720x1080,1080x1620,1280x1920&from=bu&u=vphbEyPEqiFqbeSRNQT1BVZ8ifDbQbcbA9g-NOCJVNo&cs=360x0",
    "https://sun9-12.vkuserphoto.ru/s/v1/ig2/bjDM_WPif_YT6aQmyYMjPVhw3vHENexZyD9JRj0i-zjTBSb8nDHeuX-1S1coInwkjw55aIWfrHoNTXIQAw6QRbB8.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1200x1600&from=bu&u=frbqttGM855BqaMrospPBj0L_zkqQH1HqofJ1cdBXi0&cs=540x0",
    "https://sun9-32.vkuserphoto.ru/s/v1/ig2/jCYjciyFea0NsuB9nPBdg5PusiCG0llseTVxVrO4sgY8YWi7nisHq3HJEinS9Ox9n3Fdf4g2_dOBaAbBMw3dv0OR.jpg?quality=95&as=32x44,48x66,72x99,108x148,160x219,240x329,360x493,480x658,540x740,640x877,720x987,864x1184&from=bu&u=WZJtzdBm5z0pj4Yu8IEAhmlmDbfPksmT99npBMUTPbI&cs=540x0",
    "https://sun9-81.vkuserphoto.ru/s/v1/ig2/F1AXeudzwpFpY795xX3KX2TxsFaXJFgnzQywx027y9M6RgJjPun6oyHCofdfLMa0ahQ05EW-pwr8iM1_TZWkA2a8.jpg?quality=95&as=32x48,48x72,72x108,108x162,160x240,240x360,360x540,480x720,540x810,640x960,720x1080,1080x1620,1280x1920&from=bu&u=lefiBHrbZHnnlT_1DyPYjqZwqCSIWVTMycA8mPKeL9A&cs=360x0",
    "https://sun9-59.vkuserphoto.ru/s/v1/ig2/HD5ORFi1lKfNVik071zBZlZJ_2fcg2dd8Z2USghVWU8XpldUqcSLPLAU8KLK_hS7WNepcEa6IeO65w5XnO9JQpb3.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1280x1707,1440x1920,1920x2560&from=bu&u=RXGHsKnzgRre1BdrTWhuB0-70k5Az2BnrTUxLXBeQGE&cs=540x0",
    "https://sun9-41.vkuserphoto.ru/s/v1/ig2/0wyefSWFSuYhr2MtAHSRlhYS-Gk2X373TWOct4NkEVwBqj462qXNNqByW5otzYDPIWiVlxDg5KN0aBfho5PVTQap.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1280x1707,1440x1920,1920x2560&from=bu&u=sh6vqGpgbwfMJWMTnHNpjGDBYV8MCU0Z2qaJ9_EGf0A&cs=540x0",
    "https://sun9-53.vkuserphoto.ru/s/v1/ig2/U50OTbJPdZTNWBh0RipuyslLfGCbOXFMRvaBkdlIU1oB56fxnLjz_2H_TTR94Tihhslbn08TUDMWryUkwEf9jr3W.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1280x1707,1440x1920,1920x2560&from=bu&u=4q45u9byL9MGal-1lrhvylz0_rkuq4n9xcBYLtWUvs8&cs=540x0",
    "https://sun9-5.vkuserphoto.ru/s/v1/ig2/mNyIsAaycDZi02B8DSTM72ZlekCMUqirX9DfI4kaWmbq8lrvgK8MpkNxqmZz3lH2Dfvyj9a-1253XRb7zdfkyGRu.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1280x1707,1440x1920,1920x2560&from=bu&u=tlcXfIHS5tUJqGuNA5YLj4dL6_j_pFWvQkPAjsRFnC0&cs=540x0",
    "https://sun9-10.vkuserphoto.ru/s/v1/ig2/NMrz6JlIvhLT_GgNJGDPekeq_h-SZRvfUj-rI5CsWSSn5tn5pUu14sX12A6kJ11nJM6oigZSB4Gm9sHrlbNlOfyT.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1280x1707,1440x1920,1920x2560&from=bu&u=w6JSGXOmVATFfVYUnja18DSIrcXTXxh31DB1sOmJB80&cs=540x0",
    "https://sun9-30.vkuserphoto.ru/s/v1/ig2/rHnKrM5S7YqAR7LPUyvVL1iufGDfpSIyaHr3wXlp4XyHxq86THckYjVvJyVjcbgVxUKmEXruQogAZGdqK3G1QESf.jpg?quality=95&as=32x45,48x68,72x102,108x153,160x227,240x341,360x511,480x682,540x767,640x909,720x1023,1080x1534,1280x1818,1440x2046,1802x2560&from=bu&u=cZnM0gLFlgXOjvk6msO0Tz-pKWw2FRBuSAmdGgd5fxw&cs=540x0",
    "https://sun9-68.vkuserphoto.ru/s/v1/ig2/_JuIRmBEVJ38EAplbWEspl648Py9ok7HGFvCVNXP8sElm6JT3nBJedw66UxeVNk5ASaZJZxjw8Alej0GA8acVjM5.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1280x1707,1440x1920,1920x2560&from=bu&u=ACSWQ5VcNl5gDBvR5-q5peesRdim0vU8w8IMNw2aqrU&cs=540x0",
    "https://sun9-43.vkuserphoto.ru/s/v1/ig2/KK6SLvOO81zaQY-I632baZbMElebvwvBaaiXVBrpSfe-YEkLFFyni6dJNDLj5zU0RJXIb8cnqf9Df5g1dyzSeaYX.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x854,720x960,1080x1441,1280x1708,1440x1921,1919x2560&from=bu&u=ZgREFswn7IeOVaDmncKr2_YYfOK_LZZOVGe9OReMSIQ&cs=540x0",
    "https://sun9-58.vkuserphoto.ru/s/v1/ig2/E3Gk4WuWu6WYsxYvB76VJk2dHgUpEb_RF8ENDhe6XrfgDNmfRV4MgIewM-jWgsaBpr1c91NI3QBLUU-XHSMUxYjE.jpg?quality=95&as=32x49,48x73,72x110,108x165,160x245,240x367,360x551,480x735,540x827,640x980,720x1102,1080x1654,1280x1960,1440x2205,1672x2560&from=bu&u=u50sCx_x3-fhJ6j2HOVb5SBBQ2diwxvxD04rnvS2Ra4&cs=540x0",
]

AVATAR = "https://sun1-91.vkuserphoto.ru/s/v1/ig2/Fc2uGlwK7mVa2aABhbmeheZi1QRNrKFQ4Ms0RsQv2LohhHOSxtYUHfTxkNcFc-wZpVNIVvmxm-wyzdxxLDC8pB9n.jpg?quality=95&crop=122,144,898,898&as=32x32,48x48,72x72,108x108,160x160,240x240,360x360,480x480,540x540,640x640,720x720&ava=1&u=hQIgnTMc3lLwbRS1zO5FL-vHKmliMfM8aT7Xk4LKZ7k&cs=720x720"

COVER = "https://sun9-12.vkuserphoto.ru/impf/_gnxtUzBc6nmg96_avuWrh4Gv9p4_rKnivlqEg/jG_6JckQMMo.jpg?size=1920x768&quality=95&crop=0,1065,1170,468&sign=148b8bd518cc87f967ae1f3d33294026&c_uniq_tag=OeLtI84YTRk_iGoH_h_C3pVqWjOqGkpMyaESc0SjCEs&type=cover_group"


def main():
    download(AVATAR, "logo-ava.jpg")
    download(COVER, "banner.jpg")
    for i, url in enumerate(RAW, 1):
        download(url, f"vk-{i:02d}.jpg")
    print("done")


if __name__ == "__main__":
    main()
