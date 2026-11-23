<p align="center"><img src="assets/icon.png" width="128" alt="kstack"></p>

# kstack

[English](README.md) · **Tiếng Việt**

Bộ workflow để code cùng agent trong Claude Code, đóng gói thành một plugin: các skill nhỏ gọi bằng tay, các principle dạng skill lá, một skill điều phối theo loại việc, và thói quen chứng minh mọi thay đổi chạy đúng trước khi coi là xong.

Lấy cảm hứng từ [pstack](https://github.com/cursor/plugins/tree/main/pstack) của Lauren Tan ([@poteto](https://github.com/poteto)). pstack viết cho Cursor; kstack học lại các ý tưởng đó và viết lại bằng lời của mình cho Claude Code, không chép nguyên.

> **Trạng thái:** đã có workflow dùng chung (A1–A5). Phần gắn vào từng project đang làm tiếp.

## Dùng

| Lệnh | Việc làm |
|---|---|
| `/kstack:kstack-mode <task>` | Làm task theo kiểu kstack: nhắc lại mục tiêu, chọn playbook (investigation, bug fix, feature), áp dụng principle, giao việc cho `kstack-worker`, nhờ `kstack-verifier` mới kiểm tra, commit nhỏ, không push khi chưa hỏi |
| `/kstack:sharpen <task>` | Viết lại prompt để task sâu hơn (không to hơn), dừng lại cho bạn duyệt |
| `/kstack:in-your-own-words <task>` | Nhắc lại mục tiêu, vấn đề, phạm vi và cách làm trước khi bắt tay vào |
| `/kstack:principle-<tên>` | Áp dụng riêng một principle, ví dụ `principle-explain-the-number` trước khi báo cáo một con số |

Principle có sẵn: `prove-it-works`, `fix-root-causes`, `attack-the-premise`, `smallest-change`, `verifiable-steps`, `explain-the-number`, `encode-lessons-in-structure`, `proceed-on-reversible-work`.

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
│   ├── principle-*/             # lõi: 8 principle dạng skill lá
│   └── kstack-mode/             # điều phối
│       ├── SKILL.md             #   việc bắt buộc, mục lục principle, tự chủ, subagent
│       ├── worker.md            #   luật cho mọi subagent, brief nào cũng bắt đọc trước
│       └── playbooks/           #   investigation, bug-fix, feature
├── agents/
│   ├── kstack-worker.md         # viết code theo brief
│   └── kstack-verifier.md       # kiểm tra độc lập, chỉ đọc (không có Edit/Write)
├── evals/                       # eval cho skill, chạy bằng `claude plugin eval`
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
```

## Lộ trình

- [x] **A1.** Skill nhỏ gọi bằng tay: `in-your-own-words`, `sharpen`
- [x] **A2.** 8 principle dạng skill lá
- [x] **A3.** `kstack-mode`: việc bắt buộc, mục lục principle, playbook (bug-fix, feature, investigation)
- [x] **A4.** `worker.md` và hai agent `kstack-worker`, `kstack-verifier`
- [x] **A5.** Eval cho `sharpen`: có kstack 1.00 so với 0.43 và 0.67 khi không có (2 case, mỗi case 2 lần chạy)

Sau đó là phần gắn vào từng project: verification skill, hook lint/typecheck, verifier mới cho mỗi PR, rồi tăng dần mức tự động.

## Ghi công

Ý tưởng và cấu trúc lấy từ [pstack](https://github.com/cursor/plugins/tree/main/pstack) của Lauren Tan, phát hành theo giấy phép MIT. Nếu đoạn nào trong kstack chép hoặc sửa từ văn bản của pstack, phải giữ thông báo bản quyền MIT gốc kèm theo.
