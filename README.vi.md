<p align="center"><img src="assets/icon.png" width="128" alt="kstack"></p>

# kstack

[English](README.md) · **Tiếng Việt**

Bộ workflow để code cùng agent trong Claude Code, đóng gói thành một plugin: các skill nhỏ gọi bằng tay, các principle dạng skill lá, một skill điều phối theo loại việc, và thói quen chứng minh mọi thay đổi chạy đúng trước khi coi là xong.

Lấy cảm hứng từ [pstack](https://github.com/cursor/plugins/tree/main/pstack) của Lauren Tan ([@poteto](https://github.com/poteto)). pstack viết cho Cursor; kstack học lại các ý tưởng đó và viết lại bằng lời của mình cho Claude Code, không chép nguyên.

> **Trạng thái:** đã có workflow dùng chung (A1–A5). Phần gắn vào từng project đang làm tiếp.

## Dùng

| Lệnh | Việc làm |
|---|---|
| `/kstack:kstack-mode <task>` | Làm task theo kiểu kstack: nhắc lại mục tiêu, chọn playbook (investigation, bug fix, feature, refactoring, multi-phase plan), áp dụng principle, giao việc cho `kstack-worker`, nhờ `kstack-verifier` mới kiểm tra, commit nhỏ, không push khi chưa hỏi |
| `/kstack:sharpen <task>` | Viết lại prompt để task sâu hơn (không to hơn), dừng lại cho bạn duyệt |
| `/kstack:in-your-own-words <task>` | Nhắc lại mục tiêu, vấn đề, phạm vi và cách làm trước khi bắt tay vào |
| `/kstack:principle-<tên>` | Áp dụng riêng một principle, ví dụ `principle-explain-the-number` trước khi báo cáo một con số |

22 principle chia 6 nhóm (core, design, operations and migration, verification, delegation, meta). Danh sách đầy đủ, khi nào dùng và cách mở rộng có trong [hướng dẫn](docs/guide.md) (tiếng Anh).

## Ý tưởng chính

- **Đi sâu trước, rồi mới đi nhanh.** Ít code hơn nhưng chất lượng cao hơn.
- **Agent phải tự chứng minh được.** Không có cách kiểm chứng thì người dùng thành nút thắt cổ chai.
- **Biến bài học thành cấu trúc.** Mỗi lần phải sửa agent, ưu tiên thêm type, lint, test hoặc hook thay vì thêm một dòng hướng dẫn.
- **Tin trước, song song sau.** Chỉ tăng mức tự động khi việc kiểm chứng đã đủ chắc.

## Cách tổ chức

Hai lớp:

| Lớp | Gồm | Viết theo hướng |
|---|---|---|
| Lõi | `in-your-own-words`, `sharpen`, các `principle-*` | Trung lập: không nhắc tên tool hay đường dẫn riêng của agent nào, để agent khác cũng dùng lại được |
| Điều phối | `kstack-mode`, các playbook, `worker.md`, agent, hook | Riêng cho Claude Code |

Gần như mọi skill đặt `disable-model-invocation: true`: chỉ chạy khi bạn gọi (`/kstack:<tên>`), model không tự gọi.

```
kstack/
├── .claude-plugin/plugin.json   # manifest của plugin
├── skills/
│   ├── in-your-own-words/       # lõi
│   ├── sharpen/                 # lõi
│   ├── principle-*/             # lõi: 22 principle dạng skill lá
│   └── kstack-mode/             # điều phối
│       ├── SKILL.md             #   việc bắt buộc, mục lục principle, tự chủ, subagent
│       ├── worker.md            #   luật cho mọi subagent, brief nào cũng bắt đọc trước
│       └── playbooks/           #   investigation, bug-fix, feature, refactoring, multi-phase-plan
├── agents/
│   ├── kstack-worker.md         # viết code theo brief
│   └── kstack-verifier.md       # kiểm tra độc lập, chỉ đọc (không có Edit/Write)
├── hooks/                       # hook PreToolUse: hỏi trước mọi lệnh `git push`
├── tests/                       # unit test cho hook
├── evals/                       # eval cho skill, chạy bằng `claude plugin eval`
├── scripts/check_routing.py     # kiểm tra mode chọn đúng playbook và principle
├── scripts/check_e2e.py         # chạy mode thật rồi tự kiểm tra kết quả bằng cách chạy code
├── docs/guide.md                # hướng dẫn dùng và mở rộng kstack
├── assets/                      # icon và script vẽ icon
└── CLAUDE.md                    # luật khi sửa chính kstack
```

## Cài đặt

**Phát triển trên máy mình** (đang dùng): repo nằm ở `~/Desktop/Workspace/kstack`, còn `~/.claude/skills/kstack` là symlink trỏ về đây. Claude Code tự nạp nó thành `kstack@skills-dir`.

```bash
ln -s ~/Desktop/Workspace/kstack ~/.claude/skills/kstack
```

Sửa file trong repo rồi chạy `/reload-plugins` trong phiên Claude Code là có hiệu lực.

**Thử một lần mà không cài:**

```bash
claude --plugin-dir /đường/dẫn/tới/kstack
```

Cài qua marketplace sẽ có khi repo thêm `.claude-plugin/marketplace.json`.

## Kiểm tra

```bash
claude plugin validate .            # cấu trúc plugin hợp lệ
claude plugin list                  # phải thấy kstack@skills-dir ✔ loaded
claude plugin details kstack@skills-dir   # thành phần và số token tốn thêm mỗi phiên
claude plugin eval . --runs 2 --no-publish   # eval, có nhánh không dùng plugin để so
python3 scripts/check_routing.py          # định tuyến: 8 tình huống, playbook và principle được đọc
python3 scripts/check_e2e.py              # end-to-end: sửa và commit thật, kết quả được kiểm bằng cách chạy code
python3 -m unittest discover -s tests     # unit test cho hook
```

## Thực thi bằng cấu trúc, không chỉ dặn bằng lời

kstack có một hook, nên luật "không push khi chưa được đồng ý" không còn phụ thuộc vào việc model nhớ. Lệnh Bash nào chạy `git push` cũng được xử lý theo chế độ quyền:

| Chế độ | Bạn thấy gì |
|---|---|
| default, acceptEdits, plan | Hộp xác nhận trước khi push |
| bypassPermissions, auto | Không có gì: hai chế độ này tự duyệt quyết định "ask" của hook (đã đo), nên push vẫn đi qua |
| headless (`claude -p`) | Push bị từ chối |

Khoảng hở đã biết: ở bypass và auto, luật vẫn chỉ là lời dặn cho model. Cách chặn hẳn (`deny`) ở hai chế độ này đã thử và chạy được, nhưng chưa bật cho tới khi muốn áp dụng toàn cục. Verifier không có tool Edit và Write là lớp bảo vệ bằng cấu trúc thứ hai.

## Lộ trình

- [x] **A1.** Skill nhỏ gọi bằng tay: `in-your-own-words`, `sharpen`
- [x] **A2.** 8 principle dạng skill lá
- [x] **A3.** `kstack-mode`: việc bắt buộc, mục lục principle, playbook (bug-fix, feature, investigation)
- [x] **A4.** `worker.md` và hai agent `kstack-worker`, `kstack-verifier`
- [x] **A5.** Eval cho `sharpen`: có kstack 1.00 so với 0.43 và 0.67 khi không có (2 case, mỗi case 2 lần chạy)
- [x] **A6.** Thêm 14 principle (thiết kế, vận hành và migration, điều phối, kiểm thử), playbook refactoring và multi-phase-plan, bài kiểm tra định tuyến (8/8 tình huống) và kiểm tra end-to-end (2/2)
- [x] **A7.** Hook chặn push, có unit test và thí nghiệm đối chứng; verifier từ chối làm việc nếu không có `worker.md`

Sau đó là phần gắn vào từng project: verification skill, hook lint/typecheck, verifier mới cho mỗi PR, rồi tăng dần mức tự động.

## Ghi công

Ý tưởng và cấu trúc lấy từ [pstack](https://github.com/cursor/plugins/tree/main/pstack) của Lauren Tan, phát hành theo giấy phép MIT. Nếu đoạn nào trong kstack chép hoặc sửa từ văn bản của pstack, phải giữ thông báo bản quyền MIT gốc kèm theo.
