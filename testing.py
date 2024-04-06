import csv
# from dashboard.models import Question,Answer



with open('dummydata.csv', 'r') as file:
                print('done')
                csv_reader = csv.reader(file)
                headers = next(csv_reader)  # Skipping headers if present
                
                for row in csv_reader:
                    # Assuming the CSV columns are: ID, Question, Option1, Option2, Option3, Option4
                    question_id = int(row[0])
                    question_text = row[1]
                    option_length = row[2]
                    right_option = row[3]
                    # options = row[4:8]
                    option_ends = 4 + int(option_length) # Assume 4 be the first option position
                    options = row[4:option_ends]


                    print(question_text)
                    print(options)

                    # question, created = Question.objects.get_or_create(
                    #     id=question_id,
                    #     defaults={
                    #         'question': question_text,
                    #         # Adjust other fields as needed
                    #     }
                    # )

                    for idx, option_text in enumerate(options):
                            
                            print(idx,option_text,idx + 1 == int(right_option))
                        # Answer.objects.create(
                        #     question=question,
                        #     answer=option_text,
                        #     is_right=(idx == 0)  # First option is considered the correct answer
                        # )
