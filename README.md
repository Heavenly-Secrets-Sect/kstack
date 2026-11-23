<p align="center"><img src="assets/icon.png" width="128" alt="kstack"></p>

# kstack

Bộ workflow để code cùng agent trong Claude Code, đóng gói thành một plugin: các skill nhỏ gọi bằng tay, các principle dạng skill lá, một skill điều phối theo loại việc, và thói quen chứng minh mọi thay đổi chạy đúng trước khi coi là xong.

Lấy cảm hứng từ [pstack](https://github.com/cursor/plugins/tree/main/pstack) của Lauren Tan ([@poteto](https://github.com/poteto)). pstack viết cho Cursor; kstack học lại các ý tưởng đó và viết lại bằng lời của mình cho Claude Code, không chép nguyên.

> **Trạng thái:** mới dựng khung. Các skill đang được viết dần theo lộ trình bên dưới.

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
├── skills/<tên>/SKILL.md        # mỗi skill một thư mục
├── agents/<tên>.md              # subagent
├── hooks/hooks.json             # (sau) hook dùng chung
├── evals/                       # (sau) eval cho skill, chạy bằng `claude plugin eval`
└── assets/                      # icon và script vẽ icon
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
```

## Lộ trình

- [ ] **A1.** Skill nhỏ gọi bằng tay: `in-your-own-words`, `sharpen`
- [ ] **A2.** 3–5 principle dạng skill lá
- [ ] **A3.** `kstack-mode`: việc bắt buộc, mục lục principle, playbook (bug-fix, feature, investigation)
- [ ] **A4.** `worker.md` và agent để truyền luật xuống subagent
- [ ] **A5.** Eval cho skill: rubric, model khác chấm, so với nhánh không dùng plugin

Sau đó là phần gắn vào từng project: verification skill, hook lint/typecheck, verifier mới cho mỗi PR, rồi tăng dần mức tự động.

## Ghi công

Ý tưởng và cấu trúc lấy từ [pstack](https://github.com/cursor/plugins/tree/main/pstack) của Lauren Tan, phát hành theo giấy phép MIT. Nếu đoạn nào trong kstack chép hoặc sửa từ văn bản của pstack, phải giữ thông báo bản quyền MIT gốc kèm theo.
