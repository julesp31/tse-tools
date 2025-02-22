

def get_scheduled_list(athena_query):
    list_of_words = athena_query.split()
    starting_word = "scheduled_times"
    ending_word = "}]"
    scheduled_list = []
    scheduled_boolean = False

    for word in list_of_words:
        if scheduled_boolean:
            scheduled_list.append(word)

        if starting_word in word and not scheduled_boolean:
            scheduled_boolean = True

        if ending_word in word and scheduled_boolean:
            scheduled_boolean = False

    return get_blocks(scheduled_list)


def get_blocks(busy_list):
    curly_brace_count = 0
    open_curly = '{'
    closed_curly = '}'
    blocks = []
    current_block = []

    for word in busy_list:
        if open_curly in word:
            curly_amount = 0
            for letter in word:
                if open_curly in letter:
                    curly_amount += 1
                if closed_curly in letter:
                    curly_amount -= 1
            curly_brace_count = curly_brace_count + curly_amount

        if closed_curly in word:
            curly_amount = 0
            for letter in word:
                if open_curly in letter:
                    curly_amount += 1
                if closed_curly in letter:
                    curly_amount -= 1
            curly_brace_count = curly_brace_count + curly_amount

        if curly_brace_count <= 0:
            current_block.append(word)
            blocks.append(current_block)
            current_block = []
            continue

        current_block.append(word)

    '''
    iterator = 1
    for block in blocks:
        print(str(iterator) + ' ' + str(block))
        print()
        print()
        iterator += 1
    '''
    return get_scheduled_times(blocks)


def get_scheduled_times(blocks):
    scheduled_times = {}
    block_iterator = 0
    for block in blocks:
        block_iterator += 1
        ending_word = 'end'
        ending_time = ""
        ending_boolean = False
        starting_word = 'start'
        starting_time = ""
        starting_boolean = False
        time_list = {}
        time_boolean = False
        iterator = 0

        for word in block:

            if ending_word in word or starting_word in word:
                time_boolean = True
            if time_boolean:
                iterator += 1
            if iterator == 2 and not ending_boolean:
                ending_time = word
                ending_boolean = True
                iterator = 0
                time_boolean = False
            if iterator == 2 and ending_boolean:
                starting_time = word
                iterator = 0
                time_boolean = False

        scheduled_times[starting_time] = ending_time

    return scheduled_times
