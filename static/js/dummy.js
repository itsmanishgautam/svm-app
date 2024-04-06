
        


    
     
    // validateForm(){
    //    if(this.question && this.answers) 
    //    {
    //     return true
    //    }
    //    if(!this.question){
    //     this.errors.push("Question is required!")
    //    }
    //    return false
    // },
    SubmitQuestion(e) {
        if (this.editEnable) {
          // if(this.validateForm()){
      
              axios
            .patch(
              `api/v1/question/{{category.id}}/${this.edit_question.id}/`,
              this.edit_question
            )
            .then((response) => {
              toastr.clear()
              const displaymessage = `Success !\n Questions Updated`
              toastr.warning(displaymessage, 'Updated')
              this.getQuestions()
              this.editEnable = false
            })
      
         
          return
        }
        const formData = {
          question: this.question,
          answers: this.answers,
        }
        console.log(formData)
        axios
          .post('api/v1/question/{{category.id}}/', formData)
          .then((response) => {
            console.log(response)
            // this.questions.push(response.data)
            // this adds to last of array
            // use unshift to add to the first@@
            this.questions.unshift(response.data)
      
            toastr.clear()
            const displaymessage = `Success !\n Questions created`
            toastr.success(displaymessage, 'Success')
            //  reset form
            this.question = ''
            this.answers = [
              {
                answer: '',
                is_right: false,
              },
            ]
          })
          .catch((error) => {
            console.log(error.response)
            toastr.clear()
            const data = error.response.data
            let message = ''
            data.answers.forEach((answer) => {
              message = message + `<li>${answer.answer[0]}</li>`
            })
            const displaymessage = `Error ${error.response.data.question} ${message}`
            toastr.error(displaymessage, 'Error')
          })
      }