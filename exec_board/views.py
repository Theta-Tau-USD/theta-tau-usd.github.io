from django.shortcuts import render


def exec_board(request):
    """Exec board page with officer highlights."""
    exec_members = [
        {
            'position': 'Regent',
            'name': 'Wolfgang Reighard',
            'major': 'Mechanical Engineering',
            'bio': 'Leads chapter strategy, mentoring, and professional development initiatives.',
            'photo': 'images/exec-placeholder.svg',
        },
        {
            'position': 'Vice Regent',
            'name': 'Kailani Lenert',
            'major': 'Mechanical Engineering',
            'bio': 'Coordinates committees and keeps chapter projects moving forward.',
            'photo': 'images/exec-placeholder.svg',
        },
        {
            'position': 'Treasurer',
            'name': 'Taylor Price',
            'major': 'Mechanical Engineering',
            'bio': 'Manages budgets, reimbursements, and financial planning.',
            'photo': 'images/exec-placeholder.svg',
        },
        {
            'position': 'Secretary',
            'name': 'Parker Osborne',
            'major': 'Electrical Engineering',
            'bio': 'Maintains chapter records and supports official communications.',
            'photo': 'images/exec-placeholder.svg',
        },
        {
            'position': 'Scribe',
            'name': 'Selini Matsis',
            'major': 'Mechanical Engineering',
            'bio': 'Captures meeting highlights and preserves chapter history.',
            'photo': 'images/exec-placeholder.svg',
        },
    ]
    return render(request, 'exec_board/exec_board.html', {'exec_members': exec_members})
