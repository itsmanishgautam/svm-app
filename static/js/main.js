console.log('my js loaded')


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');



function csrfSafeMethod(method){
    return ['GET','OPTIONS','HEAD','TRACE'].includes(method);
}

// $.ajaxSetup({
//     beforeSend: function (xhr,settings){
//         if(!csrfSafeMethod(settings.type) && !this.crossDomain){
//             xhr.setRequestHeader("X-CSRFToken",csrftoken)
//         }
        

//     }
// })

// document.addEventListener('DOMContentLoaded')function() {
//     toastr.options = {
//         'closeButton': true,
//         'debug': false,
//         'newestOnTop': false,
//         'progressBar': true,
//         'positionClass': 'toast-bottom-right',
//         'preventDuplicates': false,
//         'showDuration': '1000',
//         'hideDuration': '1000',
//         'timeOut': '5000',
//         'extendedTimeOut': '1000',
//         'showEasing': 'swing',
//         'hideEasing': 'linear',
//         'showMethod': 'fadeIn',
//         'hideMethod': 'fadeOut',
//     }
// });

document.addEventListener('DOMContentLoaded', function() {
    toastr.options = {
        'closeButton': true,
        'debug': false,
        'newestOnTop': false,
        'progressBar': true,
        'positionClass': 'toast-bottom-right',
        'preventDuplicates': false,
        'showDuration': '1000',
        'hideDuration': '1000',
        'timeOut': '5000',
        'extendedTimeOut': '1000',
        'showEasing': 'swing',
        'hideEasing': 'linear',
        'showMethod': 'fadeIn',
        'hideMethod': 'fadeOut'
    };
});
