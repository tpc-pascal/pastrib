import os
import random
import subprocess
from datetime import datetime, timedelta

from .base import (
    validate_repo,
    check_clean_tree,
    resolve_branch,
    ensure_git_config,
    parse_datetime,
    confirm,
    die,
    detect_signing_key,
    write_log,
    format_duration,
)

QUOTES = [
    "Trên con đường thành công không có dấu chân của kẻ lười biếng.",
    "Cách tốt nhất để dự đoán tương lai là tạo ra nó.",
    "Đừng chờ đợi cơ hội, hãy tạo ra cơ hội.",
    "Học, học nữa, học mãi.",
    "Có công mài sắt, có ngày nên kim.",
    "Thất bại là mẹ thành công.",
    "Đi một ngày đàng, học một sàng khôn.",
    "Uống nước nhớ nguồn.",
    "Ăn quả nhớ kẻ trồng cây.",
    "Một cây làm chẳng nên non, ba cây chụm lại nên hòn núi cao.",
    "Gần mực thì đen, gần đèn thì sáng.",
    "Chịu khó mài sắt, ắt có ngày nên kim.",
    "Không có gì là không thể.",
    "Thành công không phải đích đến, mà là hành trình.",
    "Đời không có mục tiêu thì như thuyền không lái.",
    "Sai lầm lớn nhất là không dám mắc sai lầm.",
    "Hãy sống như ngày mai bạn chết.",
    "Kiến tha lâu cũng đầy tổ.",
    "Ăn chắc mặc bền.",
    "Của bền tại người.",
    "Lửa thử vàng, gian nan thử sức.",
    "Chớ thấy sóng cả mà ngã tay chèo.",
    "Sự học như thuyền ngược nước, không tiến ắt lùi.",
    "Dục tốc bất đạt.",
    "Biết người biết ta, trăm trận trăm thắng.",
    "Không thầy đố mày làm nên.",
    "Học thầy không tày học bạn.",
    "Tiên học lễ, hậu học văn.",
    "Tốt gỗ hơn tốt nước sơn.",
    "Xấu người đẹp nết còn hơn đẹp người xấu nết.",
    "Một nghề cho chín còn hơn chín nghề.",
    "Có chí thì nên.",
    "Hữu xạ tự nhiên hương.",
    "Ở hiền gặp lành.",
    "Gieo gió gặt bão.",
    "Chín người mười ý.",
    "Đồng thanh tương ứng, đồng khí tương cầu.",
    "Môi hở răng lạnh.",
    "Cá không ăn muối cá ươn.",
    "Con hơn cha là nhà có phúc.",
    "Cha mẹ sinh con, trời sinh tính.",
    "Tre già măng mọc.",
    "Nước chảy đá mòn.",
    "Mưa dầm thấm lâu.",
    "Chậm mà chắc.",
    "Dám nghĩ dám làm.",
    "Sống là cho đâu chỉ nhận riêng mình.",
    "Hạnh phúc là một hành trình, không phải đích đến.",
    "Làm điều tốt, điều tốt sẽ đến với bạn.",
    "Tư duy tích cực sinh ra năng lượng tích cực.",
    "Đầu tư vào tri thức là đầu tư sinh lời nhất.",
    "Không ai vấp ngã khi nằm trên giường.",
    "Mọi thứ đều có thể nếu bạn tin.",
    "Sự kiên nhẫn là chìa khóa của thành công.",
    "Chất lượng hơn số lượng.",
    "Im lặng là vàng.",
    "Thời gian là vàng bạc.",
    "Sức khỏe là vốn quý nhất.",
    "Đoàn kết là sức mạnh.",
    "Cảm ơn đời với những gì tôi đang có.",
    "Tập trung vào mục tiêu, đừng nhìn vào chướng ngại vật.",
    "Mỗi ngày là một cơ hội mới.",
    "Hãy tử tế với người khác, và thế giới sẽ tử tế với bạn.",
    "Tự do nằm trong tâm trí bạn.",
    "Đừng so sánh mình với ai khác.",
    "Bạn mạnh mẽ hơn bạn nghĩ.",
    "Sai lầm là bài học quý giá.",
    "Không bao giờ là quá muộn để bắt đầu.",
    "Hạnh phúc là khi bạn cho đi.",
    "Bí quyết của thành công là bắt đầu.",
    "Đam mê là ngọn lửa của cuộc đời.",
    "Mỗi thử thách là một cơ hội.",
    "Sự trung thực là chính sách tốt nhất.",
    "Hãy sống thật với chính mình.",
    "Luôn học hỏi, luôn phát triển.",
    "Sự đơn giản là đỉnh cao của tinh tế.",
    "Tôn trọng người khác là tôn trọng chính mình.",
    "Lạc quan là niềm tin dẫn đến thành tựu.",
    "Hãy làm việc chăm chỉ và ước mơ lớn.",
    "Sự khác biệt tạo nên đẳng cấp.",
    "Kiên trì không phải là chạy nhanh, mà là không dừng lại.",
    "Đời ngắn lắm, hãy mỉm cười.",
    "Cho đi là nhận lại.",
    "Mỗi ngày hãy là một phiên bản tốt hơn của chính mình.",
    "Yêu thương là điều kỳ diệu nhất.",
    "Sống có mục đích, chết không hối tiếc.",
    "Trí tuệ là sức mạnh.",
    "Lòng tốt không bao giờ là lãng phí.",
    "Hãy để trái tim dẫn lối.",
    "Không gì là vĩnh viễn, hãy trân trọng từng khoảnh khắc.",
    "Học từ quá khứ, sống cho hiện tại, hướng về tương lai.",
    "Sức mạnh đến từ sự vượt khó.",
    "Nụ cười là liều thuốc tốt nhất.",
    "Đừng để nỗi sợ ngăn cản bạn.",
    "Mỗi người đều có giá trị riêng.",
    "Thế giới rộng lớn, hãy khám phá.",
    "Thay đổi là điều tất yếu của cuộc sống.",
    "Sáng tạo không có giới hạn.",
    "Đừng đánh giá cuốn sách qua bìa của nó.",
    "Tình bạn là món quà vô giá.",
    "Hãy biết ơn những điều nhỏ bé.",
    "Nghịch cảnh là bước đệm của thành công.",
    "Bình yên bắt đầu từ bên trong.",
    "Không có đường tắt đến thành công.",
    "Làm điều đúng đắn, dù không ai nhìn thấy.",
    "Giàu có thực sự là giàu tâm hồn.",
    "Cơ hội đến với những ai biết nắm bắt.",
    "Hãy luôn tiến về phía trước.",
]

EXTENSIONS = [
    ".py", ".js", ".ts", ".jsx", ".tsx", ".json", ".yaml", ".yml",
    ".toml", ".csv", ".xml", ".html", ".css", ".scss", ".less",
    ".md", ".txt", ".sh", ".bat", ".ps1", ".ini", ".cfg", ".env",
    ".sql", ".rb", ".go", ".rs", ".java", ".php", ".swift", ".kt",
    ".c", ".cpp", ".h", ".cs", ".lua", ".r", ".pl", ".dart", ".lock",
    ".vue", ".svelte", ".ex", ".exs",
]

_CONTENT_PY = [
    "def deploy_18h_chieu_thu_6():\n    print(\"cầu trời không lỗi\")\n    return None",
    "# TODO: sửa cái bug này từ tháng trước\n# TODO: vẫn chưa sửa\n# TODO: chuyển task cho intern",
    "def hotfix_production():\n    \"\"\"Chạy ẩu nhưng chạy được\"\"\"\n    pass",
    "try:\n    import solution\nexcept ImportError:\n    print(\"copy từ Stack Overflow đi\")\n    solution = None",
    "class Developer:\n    def __init__(self):\n        self.coffee = 0\n        self.mood = \"bình thường\"\n    def work(self):\n        if self.coffee < 3:\n            return \"ngáp\"\n        return \"code bug\"",
    "# Sửa bug: thêm dấu chấm phẩy\n# Bug vẫn còn\n# Hoá ra là do cache",
    "def refactor():\n    return deploy()  # refactor xong là deploy luôn",
    "if __name__ == \"__main__\":\n    print(\"chạy thử xem sao\")\n    # chạy ổn, để đó",
    "import antigravity  # let's hope it works",
    "def main():\n    while not deadline:\n        coffee()\n        code()\n        pray()",
]

_CONTENT_JS = [
    "const fixBug = () => { console.log(\"sao nó chạy???\") }",
    "// code này viết lúc 2h sáng\n// không dám động vào nữa",
    "import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react'  // thiếu cái nào thêm cái đó",
    "const [isWorking, setIsWorking] = useState(false)  // luôn false",
    "function debug() {\n    console.log(\"1\")\n    console.log(\"2\")\n    console.log(\"debug hết\")\n    // chắc bug ở đâu đó gần đây\n}",
    "var x = \"không biết var hay const\"  // thằng intern viết",
    "document.getElementById(\"root\").innerHTML = \"<h1>Deploy xong rồi</h1>\"",
    "// npx create-react-app\n// npm install\n// npm start\n// npm ERR!",
    "setTimeout(() => {\n    location.reload()  // reset khi bug\n}, 3000)",
    "export default function App() {\n    return <div>Chạy được rồi, đừng hỏi sao</div>\n}",
]

_CONTENT_TS = [
    'type Status = "working" | "broken" | "fixing" | "praying"',
    "interface Developer {\n    name: string\n    coffeeCount: number\n    isPanicking: boolean\n}",
    'const enum DeployPhase {\n    Building = "đang build",\n    Testing = "quên test",\n    Deploying = "hồi hộp",\n    Rollback = "về thôi"\n}',
    "function assertWorking(code: any): asserts code is never {\n    throw new Error(\"đã bảo chạy trên máy tao\")\n}",
    "// TypeScript không cứu được team này",
]

_CONTENT_DATA = [
    '{ "app": "pastrib", "version": "1.0.0-beta-gacha", "status": "chạy là mừng" }',
    '{ "dependencies": { "react": "^18.0.0", "common-sense": "latest" }, "scripts": { "fix": "rm -rf node_modules && npm install" } }',
    '{ "name": "project-x", "description": "chạy trên máy em mà?", "author": "intern", "license": "UNLICENSED (chạy được thì thôi)" }',
    '{ "config": { "debug": true, "strict": false, "hope": "always" } }',
    '[ { "id": 1, "bug": "null reference" }, { "id": 2, "bug": "undefined is not a function" }, { "id": 3, "bug": "unknown" } ]',
    '{ "deploy": { "time": "18h thứ 6", "strategy": "hope_for_the_best", "rollback_plan": null } }',
    'app:\n  name: pastrib\n  version: latest\n  stability: "có thể"\n\ndeploy:\n  time: "18h thứ 6"\n  mood: hồi_hộp\n  rollback: khi_cần',
    'services:\n  chay_tren_may_tao:\n    build: .\n    ports:\n      - "8080:80"\n    restart: always  # chắc chắn',
    'database:\n  host: localhost\n  port: 3306\n  username: root\n  password: "123456"  # điển hình',
    'ci:\n  test:\n    - run: npm test\n    - run: echo "qua hết test"\n  deploy:\n    - run: git push --force',
    '[pastrib]\nname = "pastrib"\nversion = "1.0.0"\ndescription = "tạo commit giả cho vui"\n\n[developer]\nmood = "lười"\ncoffee = 5\n\n[database]\nhost = "localhost"\nport = 3306',
    '[tool]\nname = "magic-fix"\ndescription = "sửa bug không cần biết bug gì"\nsafe = false',
    '[dependencies]\npastrib = { version = "*", source = "local" }\nhope = "1.0.0"',
    '<?xml version="1.0" encoding="UTF-8"?>\n<app>\n  <mode>production</mode>\n  <database>chạy_tới_chạy_lui</database>\n  <debug>true</debug>\n</app>',
    '<?xml version="1.0"?>\n<config>\n  <strategy>hope_for_the_best</strategy>\n  <rollback>none</rollback>\n</config>',
    'ngày,số_tách_cà_phê,bug_moi,bug_fix\n2024-01-01,5,12,3\n2024-01-02,8,15,2\n2024-01-03,3,8,7\n2024-01-04,6,20,1',
    'id,name,status,hours_slept\n1,"Developer A",online,2\n2,"Developer B",panic,0\n3,"Intern",crying,4',
]

_CONTENT_WEB = [
    '<div class="loading">\n    <p>Đang tải... (mãi mãi)</p>\n</div>',
    '<!-- cái này copy từ Stack Overflow -->\n<div class="magic-spacer"><!-- xóa là hỏng -->&nbsp;</div>',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">',
    '<script>\n    console.log("nếu bạn đọc được cái này thì bug vẫn còn")\n</script>',
    '<h1>Chào mừng đến với trang web</h1>\n<p>Trang web đang được xây dựng (từ 2 năm trước)</p>',
    '<button onclick="fixEverything()">Bấm để sửa lỗi</button>',
    '<!-- TODO: responsive -->\n<!-- TODO: accessibility -->\n<!-- TODO: thôi kệ -->',
    '<nav>\n    <a href="/">Trang chủ</a>\n    <a href="/about">Về chúng tôi</a>\n    <a href="/bug">Báo lỗi</a>\n</nav>',
    '.btn-primary {\n    background: #FF0000; /* đỏ cho chắc */\n    color: white;\n    border: none;\n}',
    '.magic-fix {\n    display: none; /* khi không biết sửa thì ẩn nó đi */\n}',
    '/* !important vì không quan tâm specificity */\n.text-center {\n    text-align: center !important;\n}',
    '@media (max-width: 768px) {\n    .bug {\n        display: none; /* mobile first: ẩn lỗi trên mobile */\n    }\n}',
    '.container {\n    width: 100%;\n    max-width: 1200px;\n    margin: 0 auto;\n    /* padding: chờ designer */\n}',
    '/* style này của thằng intern */\ndiv {\n    border: 1px solid red; /* debug */\n}\n/* quên xóa debug */',
    '.loading-spinner {\n    animation: spin 2s linear infinite;\n    /* chạy mãi mãi */\n}',
]

_CONTENT_SCRIPT = [
    'echo "đang deploy..."\nnpm run build\necho "xong (chắc vậy)"',
    '#!/bin/bash\n# script này có thể chạy hoặc không\n# tuỳ tâm trạng của máy\n\ngit add .\ngit commit -m "cầu may"\ngit push --force',
    'while true; do\n    curl -s http://localhost:8080/health || echo "chết rồi"\n    sleep 5\ndone',
    '# Đừng chạy file này nếu không biết nó làm gì\n# (tôi cũng không biết)\nrm -rf /tmp/*',
    '#!/usr/bin/env bash\nset -e  # fail nhanh, fail gọn\necho "building..."\nnpm run build 2>/dev/null || echo "thôi kệ"',
    '# source: được copy từ Stack Overflow\n# tác giả: không rõ\n# lý do: thấy nó chạy',
    'echo "checking dependencies..."\nsleep 2\necho "done (chắc thế)"',
    'docker ps | grep my-app | awk \'{print $1}\' | xargs docker kill  # kill all',
    '#!/bin/bash\npip install -r requirements.txt  # hy vọng không conflict',
    '@echo off\necho Dang deploy...\nnpm run build\nif %errorlevel% neq 0 (\n    echo "Bug roi"\n    pause\n)',
    '@echo off\necho May tinh dang chay cham\npause\nexit',
    '@echo off\n:: Script nay chay duoc tren may toi\n:: Khong dam bao tren may khac\nnode app.js',
    '@echo off\necho Cai dat phu thuoc...\nnpm install\nif %errorlevel% equ 0 (echo "Xong") else (echo "Thu lai")',
    'Write-Host "Đang deploy..." -ForegroundColor Yellow\nnpm run build\nif ($?) { Write-Host "Xong!" } else { Write-Host "Thôi chết" -ForegroundColor Red }',
    '$bug = Get-ChildItem -Recurse -Filter "*.bug" | Select-Object -First 1\nif ($bug) { Get-Content $bug.FullName } else { Write-Host "Hôm nay không có bug, lạ" }',
    'function Fix-Everything {\n    param([switch]$Force)\n    Write-Host "Đang sửa hết..."\n    if ($Force) { rm -Recurse -Force node_modules }\n}',
]

_CONTENT_CONFIG = [
    "[app]\nname = Pastrib\nversion = 1.0.0\ndebug = true\n\n[developer]\nmood = lười\nlunch_time = 12:00\n\n[database]\nhost = localhost\nport = 3306\nuser = root\npass = admin",
    "[DEFAULT]\n# Config mặc định, đừng sửa nếu không biết\n\n[logging]\nlevel = DEBUG\nfile = /dev/null  # không log gì cả",
    "[user]\nname = Developer\nskill = \"copy paste\"\nexperience = \"5 năm (1 năm kinh nghiệm, lặp lại 5 lần)\"",
    "[remote]\nurl = https://github.com/username/project\nbranch = main  # hoặc master, tuỳ hứng",
    "[deploy]\ntime = \"18:00 Friday\"\nritual = \"cầu nguyện\"\nbackup = false",
    "DATABASE_URL=mysql://root:123456@localhost:3306/mydb\nSECRET_KEY=secret123  # đổi sau (từ 2 năm trước)\nDEBUG=true\nAPI_KEY=sk-xxxxxxxxxxxxxxxxxxxxx",
    "NODE_ENV=development  # production == bug\nPORT=3000\nHOST=0.0.0.0\nLOG_LEVEL=error",
    "# Copy .env.example thành .env\n# Rồi sửa cho phù hợp\n# (ai cũng làm thế chứ gì)\nDB_PASS=changeme",
    "# Không push .env lên git nhé\n# (thằng intern push rồi)\nGITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxx",
    "# Lock file này đảm bảo... không ai biết đảm bảo gì\n# Chỉ biết xóa là hỏng\n\npastrib==1.0.0\nhope==latest\ncoffee==5.0.0",
    "# This lock file was auto-generated\n# (nó tự sinh ra, tự biến mất, tự xuất hiện lại)\n\nsolution==0.0.1  # không có thật",
]

_CONTENT_SQL = [
    "-- Chạy câu lệnh này nếu muốn xoá hết dữ liệu\n-- (không trách tôi nhé)\nDROP DATABASE IF EXISTS production;\nCREATE DATABASE production;",
    "SELECT * FROM users WHERE email = 'admin@example.com';\n-- ủa sao không có kết quả?\n-- À, database mới tạo, chưa có data",
    "CREATE TABLE IF NOT EXISTS bugs (\n    id INT AUTO_INCREMENT PRIMARY KEY,\n    description TEXT,\n    status ENUM('open', 'fixed', 'wontfix') DEFAULT 'open',\n    reported_by VARCHAR(100) DEFAULT 'intern'\n);",
    "-- Optimize query:\n-- SELECT * FROM big_table WHERE 1=1  -- nhanh hơn?",
    "INSERT INTO commits (message, bug_count) VALUES ('fix bug', 5), ('add feature', 12), ('refactor', 99);",
    "UPDATE developers SET is_panicking = 1 WHERE day_of_week = 'Friday' AND hour >= 17;",
]

_CONTENT_DOC = [
    "## Hướng dẫn cài đặt nhanh\n\n> Chạy cái lệnh dưới đây. Nếu lỗi thì chạy lại lần nữa.\n\n```bash\nnpm install\nnpm start\n```",
    "## FAQ\n\n**Q: Code không chạy?**\nA: Thử `rm -rf node_modules && npm install`.\n\n**Q: Vẫn không chạy?**\nA: Restart máy.",
    "## Lưu ý khi deploy\n\n- Đừng deploy lúc 18h thứ 6\n- Nếu deploy thì cầu trời\n- Luôn có sẵn cà phê",
    "# Changelog\n\n## [1.0.0] - 2024-01-01\n### Added\n- Bug mới\n- Deadline stress\n\n### Fixed\n- Bug cũ (tạo bug mới)",
    '> "Nó chạy trên máy tao mà?"\n> — Mọi lập trình viên',
    "## API Documentation\n\nGET /api/random\n→ Trả về lỗi ngẫu nhiên",
    "## TODO\n\n- [ ] Viết test\n- [ ] Đọc document\n- [ ] Nghỉ việc",
    "Cách tốt nhất để sửa bug là tạo thêm bug mới.",
    "Hôm nay code chạy, mai không biết. Tận hưởng khoảnh khắc này.",
    "Chạy trên máy tao mà? Để tao check lại... à ờ, chạy thiệt.",
    "Deploy lúc 17h50 thứ 6. Xin lỗi thứ 2 của tuần sau.",
    "Refactor? Không, rename thôi.",
    "Bug hôm nay = Feature của ngày mai.",
    "Production bug? Hotfix. Production crash? Weekend.",
    "Code chạy là mừng, còn bug là tính năng bí mật.",
    'Interview: "Em biết clean code" / Thực tế: `it works; don\'t touch`',
    'Semantic versioning? Tôi chỉ biết "chạy" vs "không chạy".',
    'npm install: tải 1500 packages để in "Hello World"',
    'Git commit thường kèm "chắc chạy", "maybe fix", "test", "update"',
    "Pull request: 1 dòng code, 100 comment.",
]

_CONTENT_OTHER = [
    "def deploy\n  puts \"Cầu trời...\"\n  sleep(rand(10..60))\n  puts \"Xong (chắc thế)\"\nend",
    "class Developer\n  attr_accessor :coffee, :mood\n  def initialize\n    @coffee = 5\n    @mood = :normal\n  end\nend",
    "package main\n\nfunc main() {\n    println(\"Chạy được rồi, đừng hỏi sao\")\n}",
    "func Deploy() error {\n    return fmt.Errorf(\"chưa kịp test\")\n}",
    "type Config struct {\n    Debug bool   `json:\"debug\"`\n    Hope  string `json:\"hope\"`\n}",
    "fn main() {\n    println!(\"Nó compile được? Bất ngờ chưa!\");\n}",
    "struct Developer {\n    coffee_count: u32,\n    is_caffeinated: bool,\n}",
    'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Xin chào, cả nhà cùng bug!");\n    }\n}',
    "class Bug {\n    private String description;\n    private Severity severity;\n    private Developer assignee;\n}",
    "<?php\n// Code này chạy trên PHP 5.6\n// Đừng hỏi sao vẫn chưa upgrade\necho \"Nó chạy mà?\";\n?>",
    'import UIKit\n\nclass ViewController: UIViewController {\n    override func viewDidLoad() {\n        super.viewDidLoad()\n        print("Xin chào iOS (và bug)")\n    }\n}',
    "fun main() {\n    println(\"Kotlin: Java nhưng ngầu hơn\")\n}",
    "#include <stdio.h>\n\nint main() {\n    printf(\"Hello, Bug!\\n\");\n    return 0;\n}",
    "#include <iostream>\n\nint main() {\n    std::cout << \"C++: mạnh mẽ, phức tạp, đau đầu\" << std::endl;\n    return 0;\n}",
    "using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine(\"Xin chào .NET\");\n    }\n}",
    '-- Code này chạy trên Luau (Roblox)\nprint("Xin chào, bug ơi!")',
    'void main() {\n  print(\'Dart: Flutter mà, chạy mượt\');\n}',
    'IO.puts("Elixir: functional, concurrent, bug cũng concurrent")',
]

_CONTENT_MAP = {
    ".py": _CONTENT_PY,
    ".js": _CONTENT_JS,
    ".ts": _CONTENT_TS,
    ".jsx": _CONTENT_JS,
    ".tsx": _CONTENT_JS,
    ".vue": _CONTENT_JS,
    ".svelte": _CONTENT_JS,
    ".html": _CONTENT_WEB,
    ".css": _CONTENT_WEB,
    ".scss": _CONTENT_WEB,
    ".less": _CONTENT_WEB,
    ".json": _CONTENT_DATA,
    ".yaml": _CONTENT_DATA,
    ".yml": _CONTENT_DATA,
    ".toml": _CONTENT_DATA,
    ".csv": _CONTENT_DATA,
    ".xml": _CONTENT_DATA,
    ".sh": _CONTENT_SCRIPT,
    ".bat": _CONTENT_SCRIPT,
    ".ps1": _CONTENT_SCRIPT,
    ".ini": _CONTENT_CONFIG,
    ".cfg": _CONTENT_CONFIG,
    ".env": _CONTENT_CONFIG,
    ".lock": _CONTENT_CONFIG,
    ".md": _CONTENT_DOC,
    ".txt": _CONTENT_DOC,
    ".sql": _CONTENT_SQL,
    ".rb": _CONTENT_OTHER,
    ".go": _CONTENT_OTHER,
    ".rs": _CONTENT_OTHER,
    ".java": _CONTENT_OTHER,
    ".php": _CONTENT_OTHER,
    ".swift": _CONTENT_OTHER,
    ".kt": _CONTENT_OTHER,
    ".c": _CONTENT_OTHER,
    ".cpp": _CONTENT_OTHER,
    ".h": _CONTENT_OTHER,
    ".cs": _CONTENT_OTHER,
    ".lua": _CONTENT_OTHER,
    ".r": _CONTENT_OTHER,
    ".pl": _CONTENT_OTHER,
    ".dart": _CONTENT_OTHER,
    ".ex": _CONTENT_OTHER,
    ".exs": _CONTENT_OTHER,
}


def _generate_content(ext):
    pool = _CONTENT_MAP.get(ext, _CONTENT_DOC)
    return random.choice(pool)


def _count_commits_on_date(repo, date):
    after = date.strftime("%Y-%m-%d 00:00:00")
    before = (date + timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
    r = subprocess.run(
        ["git", "rev-list", "--count", "--after", after, "--before", before, "HEAD"],
        cwd=repo, capture_output=True, text=True, check=False,
    )
    if r.returncode != 0:
        return 0
    return int(r.stdout.strip())


def _create_dummy_commits(repo, date, count, can_sign, run_date=None):
    run_date = run_date or datetime.now().strftime("%Y-%m-%d")
    dummy_dir = os.path.join(repo, "dummy", run_date)
    os.makedirs(dummy_dir, exist_ok=True)

    date_str = date.strftime("%Y-%m-%d")
    ext = random.choice(EXTENSIONS)
    file_path = os.path.join("dummy", run_date, f"{date_str}{ext}")
    full_path = os.path.join(repo, file_path)

    day_ts = int(datetime(date.year, date.month, date.day).timestamp())

    for _ in range(count):
        hour = random.randint(8, 18)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        commit_ts = day_ts + hour * 3600 + minute * 60 + second

        content = _generate_content(ext)

        with open(full_path, "a", encoding="utf-8") as f:
            f.write(f"{content}\n\n")

        subprocess.run(
            ["git", "add", "-f", file_path],
            cwd=repo, check=True,
        )

        cmd = ["git", "commit"]
        if can_sign:
            cmd.append("-S")
        cmd.extend([
            "-m", f"daily: {date_str}",
        ])

        subprocess.run(
            cmd,
            cwd=repo, check=True,
            env={
                **os.environ,
                "GIT_AUTHOR_DATE": f"{commit_ts} +0700",
                "GIT_COMMITTER_DATE": f"{commit_ts} +0700",
            },
        )


def run(start_date, end_date, branch=None, yes=False, dry_run=False, run_date=None):
    validate_repo(".")
    start_time = datetime.now()
    if not yes:
        check_clean_tree(".")
    branch = resolve_branch(".", branch)

    start_dt = parse_datetime(start_date)
    end_dt = parse_datetime(end_date)

    if start_dt > end_dt:
        die("start-date must be earlier than end-date.")

    current = start_dt
    total_days = (end_dt - start_dt).days + 1
    print(f"Scanning {total_days} days from {start_date} to {end_date}...")
    print(f"Branch: {branch}")

    ensure_git_config(".")
    can_sign = detect_signing_key(".")
    if can_sign:
        print("GPG signing key detected - new commits will be signed.")

    created_total = 0
    days_filled = 0
    days_skipped = 0
    day_idx = 0

    while current <= end_dt:
        day_idx += 1

        count = _count_commits_on_date(".", current)

        if count > 0:
            print(f"  [{day_idx}/{total_days}] {current.strftime('%Y-%m-%d')}: SKIP ({count} existing)")
            days_skipped += 1
        else:
            n_commits = random.randint(2, 3)
            if dry_run:
                print(f"  [{day_idx}/{total_days}] {current.strftime('%Y-%m-%d')}: would create {n_commits} commits")
            else:
                _create_dummy_commits(".", current, n_commits, can_sign, run_date)
                print(f"  [{day_idx}/{total_days}] {current.strftime('%Y-%m-%d')}: {n_commits} commits")
            days_filled += 1
            created_total += n_commits

        current += timedelta(days=1)

    end_time = datetime.now()
    duration = end_time - start_time

    print()
    if dry_run:
        print(f"[DRY RUN] Would create ~{created_total} commits across {days_filled} days.")
    else:
        write_log(".", [
            f"=== Run: {start_time.strftime('%Y-%m-%d %H:%M:%S')} → {end_time.strftime('%H:%M:%S')} ({format_duration(duration)}) ===",
            f"  Mode:       spread",
            f"  Branch:     {branch}",
            f"  Range:      {start_date} → {end_date}",
            f"  Days:       {total_days} total / {days_filled} filled / {days_skipped} skipped",
            f"  Commits:    {created_total} created",
            f"  Status:     Success",
            "─" * 55,
        ])
        print(f"Done! Created {created_total} commits across {days_filled} days.")
        print(f"Skipped {days_skipped} days with existing commits.")
        print()
        print("To push to remote:")
        print(f"    git push origin {branch}")
        print()
