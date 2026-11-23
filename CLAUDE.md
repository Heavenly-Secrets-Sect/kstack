# kstack

Plugin Claude Code chứa workflow code cùng agent, học từ pstack của Lauren Tan (bản tham khảo: `github.com/cursor/plugins/tree/main/pstack`). File này là luật khi **sửa chính kstack**; nó không đi theo plugin tới người dùng.

`~/.claude/skills/kstack` là symlink trỏ về repo này, nên Claude Code nạp kstack thành `kstack@skills-dir`. Sửa xong chạy `/reload-plugins`.

## Hai lớp

- **Lõi** (`in-your-own-words`, `sharpen`, `principle-*`): trung lập, không nhắc tên tool hay đường dẫn riêng của agent nào.
- **Điều phối** (`kstack-mode` cùng `worker.md` và `playbooks/`, `agents/`): viết riêng cho Claude Code, dùng tên tool thật.

## Viết skill

- Mỗi skill một ý, ngắn: principle khoảng 10 dòng, playbook dưới 25 dòng.
- Mặc định `disable-model-invocation: true`. Skill đó không gọi được qua Skill tool, nên mode đọc nó bằng đường dẫn `${CLAUDE_SKILL_DIR}/../<tên>/SKILL.md`.
- `${CLAUDE_SKILL_DIR}` và `$ARGUMENTS` chỉ được thay trong `SKILL.md`, không thay trong playbook hay `worker.md`.
- Viết lại bằng lời của mình, không chép nguyên văn pstack. Đoạn nào chép thì phải kèm thông báo MIT của pstack.
- Thêm principle mới thì thêm luôn một dòng vào mục lục trong `skills/kstack-mode/SKILL.md`.
- Một lỗi agent lặp lại thì sửa bằng cấu trúc trước (giới hạn tool, luật cụ thể kèm cách thay thế), sau đó mới tới câu chữ. Ví dụ: verifier từng chạy `git checkout` nên giờ có luật cấm kèm cách thay thế.

## Kiểm tra trước khi commit

```bash
claude plugin validate .                        # cấu trúc hợp lệ
claude plugin details kstack@skills-dir         # token tốn mỗi phiên (hiện khoảng 850)
claude -p "/kstack:<skill> <task mẫu>"          # chạy thử một skill trong thư mục nháp
claude plugin eval . --runs 2 --no-publish      # eval, có nhánh không-plugin để so
```

Sửa skill nào có eval thì chạy lại eval đó (`--case <tên>`). Điểm "có plugin" không được giảm.

## Commit

Commit nhỏ, mỗi commit một bước và để repo ở trạng thái chạy được. Danh tính repo là `KiRzEa <kietnt0603@gmail.com>`, đã đặt trong cấu hình git cục bộ. Không push khi chưa được đồng ý.
