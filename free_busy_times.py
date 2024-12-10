

def get_busy_list(athena_query):
    list_of_words = athena_query.split()
    starting_word = "free_busy_data"
    ending_word = "}}],"
    busy_list = []
    busy_boolean = False

    for word in list_of_words:
        if busy_boolean:
            busy_list.append(word)

        if starting_word in word and not busy_boolean:
            busy_boolean = True

        if ending_word in word and busy_boolean:
            busy_boolean = False

    return get_blocks(busy_list)


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

        if curly_brace_count == 0:
            current_block.append(word)
            blocks.append(current_block)
            current_block = []
            continue

        current_block.append(word)

    '''
    # Printing Each Block
    iterator = 1
    for block in blocks:
        print(str(iterator) + ' ' + str(block))
        print()
        print()
        iterator += 1
    '''
    return get_busy_times(blocks)


def get_busy_times(blocks):
    busy_times = {}
    block_iterator = 0
    for block in blocks:
        block_iterator += 1
        ending_word = 'End'
        ending_time = ""
        ending_boolean = False
        starting_word = 'Start'
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
            if iterator == 3 and not ending_boolean:
                ending_time = word
                # print("Ending Time: " + ending_time)
                ending_boolean = True
                iterator = 0
                time_boolean = False
            if iterator == 3 and ending_boolean:
                starting_time = word
                # print("Starting Time: " + starting_time)
                iterator = 0
                time_boolean = False

        busy_times[starting_time] = ending_time

    return busy_times
