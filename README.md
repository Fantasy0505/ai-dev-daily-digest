# AI 涓庡紑鍙戣€呯儹鐐规棩鎶?
杩欐槸涓€涓畬鍏ㄦ墭绠″湪 GitHub Actions 涓婄殑 Python 鑷姩鍖栭」鐩€傚畠姣忓ぉ鏀堕泦杩?24 灏忔椂鐨?AI銆佽绠楁満銆佺紪绋嬨€佸紑婧愪笌寮€鍙戣€呭伐鍏峰姩鎬侊紝浣跨敤 OpenAI 鐢熸垚涓枃鎽樿锛屽苟閫氳繃 Resend 鍙戦€佷竴灏侀€傞厤 Outlook 鐨?HTML 閭欢銆?
浠诲姟鐢?GitHub 鎵樼鐨勮繍琛屽櫒鎵ц锛?*鐢佃剳鍏虫満銆佷紤鐪犳垨鏂綉閮戒笉浼氬奖鍝嶆墽琛?*銆傚彧瑕?GitHub 浠撳簱銆丄ctions 鍜屾墍闇€瀵嗛挜浠嶅彲鐢紝宸ヤ綔娴佷細缁х画杩愯銆?
## 宸ヤ綔娴?
1. 骞惰璇诲彇 OpenAI銆丟oogle AI銆丄nthropic銆丮icrosoft Developer銆丟itHub銆丳ython銆丷ust銆並ubernetes 鐨勫叕寮€ RSS銆?2. 璇诲彇 GitHub Search API 涓柊寤轰笖鏈夌儹搴︾殑浠撳簱锛屼互鍙?Hacker News 鐑棬鎶€鏈晠浜嬨€?3. 浠呬繚鐣欏彂甯冩椂闂村湪鏈€杩?24 灏忔椂鍐呫€佷富棰樼浉鍏充笖闈炴槑鏄炬帹骞跨殑鏉＄洰锛涙寜鏉ユ簮鍙俊搴︺€佷富棰樼浉鍏冲害鍜岀ぞ鍖虹儹搴︽帓搴忋€佸幓閲嶏紝鏈€澶氶€夋嫨 12 鏉°€?4. 鍚?OpenAI 鎻愪緵鏍囬銆佹潵婧愩€佹椂闂翠笌鏉ユ簮鎽樺綍锛涙ā鍨嬪彧鑳芥嵁姝ょ紪鍐欎腑鏂囨爣棰樸€?鈥? 鍙ユ憳瑕佸拰鏍囩銆傚師濮嬮摼鎺ヤ笌鏉ユ簮涓嶄細浜ょ粰妯″瀷鏀瑰啓銆?5. 娓叉煋 HTML 骞堕€氳繃 Resend API 鍙戣嚦寰蒋閭銆?
褰撴柊闂绘簮鐭殏涓嶅彲鐢ㄦ椂锛屽叾浠栨潵婧愪細缁х画鎵ц锛涘綋妯″瀷璋冪敤澶辫触鏃讹紝閭欢浼氭槑纭爣娉ㄤ负鈥滃熀浜庢潵婧愬師鏂団€濈殑鍏滃簳鍐呭锛岀粷涓嶄吉閫犳憳瑕併€?
## 閮ㄧ讲鍒?GitHub

1. 灏嗘湰鐩綍鎺ㄩ€佽嚦涓€涓?GitHub 浠撳簱銆?2. 鍦ㄤ粨搴撲腑杩涘叆 **Settings 鈫?Secrets and variables 鈫?Actions 鈫?New repository secret**锛屾坊鍔犱互涓?Secrets锛?
| Secret | 蹇呭～ | 璇存槑 |
| --- | --- | --- |
| `OPENAI_API_KEY` | 鏄?| OpenAI API 瀵嗛挜銆?|
| `RESEND_API_KEY` | 鏄?| Resend 鐨?API 瀵嗛挜銆?|
| `SENDER_EMAIL` | 鏄?| Resend 涓凡楠岃瘉鍩熷悕涓嬬殑鍙戜欢浜猴紝渚嬪 `AI 鏃ユ姤 <digest@example.com>`銆?|
| `RECIPIENT_EMAIL` | 鏄?| 浣犵殑寰蒋鏀朵欢閭锛屼緥濡?`name@outlook.com`銆?|
| `OPENAI_MODEL` | 鍚?| 瑕嗙洊榛樿妯″瀷锛涙湭閰嶇疆鏃朵娇鐢?`gpt-4.1-mini`銆傝濉綘璐︽埛鍙敤鐨勬ā鍨嬨€?|

3. 鍦?Resend 涓坊鍔犲苟楠岃瘉浣犵殑鍙戜欢鍩熷悕锛岀劧鍚庢寜鍏?DNS 鎸囧紩娣诲姞 SPF/DKIM 璁板綍銆傜敓浜х幆澧冧腑锛宍SENDER_EMAIL` 蹇呴』浣跨敤璇ュ凡楠岃瘉鍩熷悕锛涘惁鍒?Resend 浼氭嫆缁濆彂閫佹垨鍙厑璁稿彈闄愮殑娴嬭瘯鏀朵欢浜恒€?4. 鎵撳紑浠撳簱鐨?**Actions** 椤甸潰锛岄€夋嫨 **Daily Chinese Tech Digest**锛岀偣鍑?**Run workflow** 娴嬭瘯銆傚厛纭閭欢鑳藉埌杈?Outlook锛屽啀绛夊緟瀹氭椂浠诲姟銆?
## 瀹氭椂鏃堕棿涓庡彲闈犳€?
`.github/workflows/daily-digest.yml` 浣跨敤 `0 0 * * *`銆侴itHub Actions 鐨?cron 浣跨敤 UTC锛孶TC 00:00 姝ｅソ鏄寳浜椂闂达紙UTC+8锛?8:00锛屼腑鍥芥病鏈夊浠ゆ椂銆?
GitHub 鎵樼璋冨害閫氬父浼氬湪璇ユ椂鐐瑰惎鍔紝浣嗗叕鍏?GitHub Actions 鐨?scheduled workflow 鍙兘鍥犲钩鍙拌礋杞借€岀◢鏈夊欢杩燂紱瀹冧笉鏄弗鏍煎疄鏃惰皟搴︺€傜數鑴戠姸鎬佷笉鍙備笌璇ユ祦绋嬨€?
鑻ヤ粨搴撴槸鍏紑浠撳簱涓旇繛缁?60 澶╂病鏈変换浣曚粨搴撴椿鍔紝GitHub 鍙兘鑷姩鍋滅敤 scheduled workflow銆傝闀挎湡淇濇寔姣忔棩鎶曢€掞紝璇峰畾鏈熸煡鐪?Actions 椤甸潰骞堕噸鏂板惎鐢ㄨ鍋滅敤鐨勫伐浣滄祦锛涜闂茬疆瑙勫垯鍦?GitHub 鏂囨。涓槑纭拡瀵瑰叕寮€浠撳簱銆?
## 鏈湴杩愯

闇€瑕?Python 3.11+锛?
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

鍦?`.env` 涓～鍐欒嚜宸辩殑鍊煎悗锛屽皢鍏跺姞杞借繘褰撳墠 PowerShell 浼氳瘽锛堟垨浣跨敤浣犳儻鐢ㄧ殑鐜鍙橀噺宸ュ叿锛夛紝鐒跺悗杩愯锛?
```powershell
python -m src.main
```

`.env` 宸茶 `.gitignore` 蹇界暐锛岀粷涓嶈兘鎻愪氦瀵嗛挜銆傜▼搴忔湰韬笉鑷姩璇诲彇 `.env`锛岄伩鍏嶅湪 GitHub 涓婃贩娣?Secrets锛涙湰鍦板彲浠ユ墜宸ヨ缃幆澧冨彉閲忥紝鎴栦娇鐢ㄤ綘鑷繁鐨勫畨鍏ㄥ姞杞芥柟寮忋€?
## 鎺掓煡

- **宸ヤ綔娴佸湪閰嶇疆闃舵澶辫触**锛氭牳瀵瑰洓涓繀濉?Secrets 鍚嶇О鏄惁瀹屽叏涓€鑷达紝閲嶆柊浠?Actions 椤甸潰鎵嬪姩杩愯銆?- **Resend 杩斿洖 403 鎴?422**锛氶€氬父鏄彂浠跺煙鍚嶆湭楠岃瘉銆佸彂浠朵汉鍦板潃涓嶅睘浜庤鍩熷悕锛屾垨娴嬭瘯璐﹀彿娌℃湁鑾峰噯鍚戣鏀朵欢浜哄彂淇°€?- **鏀朵笉鍒?Outlook 閭欢**锛氭鏌ュ瀮鍦鹃偖浠?鈥滃叾浠栤€濇敹浠剁锛屽苟纭鍩熷悕 SPF/DKIM 楠岃瘉宸插畬鎴愩€?- **閭欢椤圭洰杈冨皯**锛氶」鐩弗鏍奸檺鍒跺湪杩?24 灏忔椂銆佸彲淇′笖鐩稿叧鐨勫唴瀹癸紱瀹冨畞鍙皯鍙戯紝涔熶笉浼氫负浜嗗噾鏁拌€岀紪閫犵儹鐐广€?- **鏌愪釜鏂伴椈婧愬け璐?*锛氭煡鐪?GitHub Actions 鏃ュ織銆傚崟涓潵婧愬け璐ュ彧浼氳褰?warning锛屼笉浼氫腑鏂叾浠栨潵婧愭垨閭欢鎶曢€掋€?- **OpenAI 鎽樿澶辫触**锛氭棩蹇椾細璁板綍鍘熷洜锛涢偖浠朵細鍙戦€佸彲鏍搁獙鐨勫師濮嬫潵婧愬厹搴曞唴瀹广€傜‘璁?API Key銆佹ā鍨嬪悕鍜岃处鎴烽搴︺€?
## 瀹夊叏杈圭晫

椤圭洰涓嶅寘鍚湡瀹炲瘑閽ワ紝涔熶笉鍐欏叆鎴栬緭鍑哄瘑閽ャ€侴itHub Actions 浠呮巿浜?`contents: read` 鏉冮檺锛屽瘑閽ュ彧閫氳繃 Actions Secrets 娉ㄥ叆杩愯鐜銆?