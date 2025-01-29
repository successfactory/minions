FILE_PATH = "results.csv"
NAME_COLUMN = "Name"
ESTIMATED_COLUMN = "Geschätzte Zeit"
ACTUAL_COLUMN = "Tatsächliche Zeit"
DIFF_COLUMN = "Differenz (Sekunden)"


def seconds_to_mmss(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"


def mmss_to_seconds(mmss):
    try:
        minutes, seconds = map(int, mmss.split(":"))
        return minutes * 60 + seconds
    except ValueError:
        return None


def calculate_diff(estimated_time, actual_time):
    if estimated_time is None or actual_time is None:
        return None
    est_seconds = mmss_to_seconds(estimated_time)
    act_seconds = mmss_to_seconds(actual_time)
    return abs(est_seconds - act_seconds)


def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"
