# GH-graph-automation-CLI
automating GH graphs and scheduling repository pushing. the program takes your local repository and pushes it to github over the period of a few days instead of uploading everything at once


PROGRAM GitHubContributionGraph

    INPUT:
        repository_path
        chunk_size
        commits_per_day
        start_time
        interval_between_commits

    ─────────────────────────────────────
    1. INITIALIZE
    ─────────────────────────────────────

    validate repository_path

    IF repository_path is not a git repository:
        print error
        exit

    load configuration

    calculate repository contents


    ─────────────────────────────────────
    2. READ REPOSITORY
    ─────────────────────────────────────

    files = get all files in repository

    FOR each file:
        read file contents

        divide contents into chunks
            each chunk ≈ chunk_size lines

        store chunks


    ─────────────────────────────────────
    3. CREATE COMMIT PLAN
    ─────────────────────────────────────

    total_chunks = number of chunks

    commits_per_day = user setting

    calculate number of required days

    FOR each chunk:

        assign chunk to a commit

        assign commit to a day

        assign commit a time


    ─────────────────────────────────────
    4. PREVIEW
    ─────────────────────────────────────

    display:

        repository
        total files
        total lines
        total chunks
        commits per day
        estimated duration

    ask user:

        "Start? [y/N]"

    IF user says no:
        exit


    ─────────────────────────────────────
    5. EXECUTE
    ─────────────────────────────────────

    FOR each scheduled commit:

        wait until scheduled time

        take next chunk

        apply chunk to working repository

        git add changed files

        git commit with generated message

        git push

        display:
            commit number
            progress
            next scheduled commit


    ─────────────────────────────────────
    6. FINISH
    ─────────────────────────────────────

    print:
        "All chunks have been committed."

END PROGRAM