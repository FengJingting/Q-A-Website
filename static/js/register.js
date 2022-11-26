function bindCaptchaBtnClick(){
    $("#captcha-btn").on("click",function(event){
        var $this = $(this);
        var email = $("input[name='email']").val();
        if(!email){
            alert("Please input your Email！");
            return;
        }
        $.ajax({
            url: "/user/captcha",
            method: "POST",
            data: {
                "email": email
            },
            success: function (res){
                var code = res['code'];
                if(code == 200){
                    // off some click event
                    $this.off("click");
                    // start countdown
                    var countDown = 60;
                    var timer = setInterval(function (){
                        countDown -= 1;
                        if(countDown > 0){
                            $this.text(countDown+"s");
                        }else{
                            $this.text("Get Captcha");
                            bindCaptchaBtnClick();
                            clearInterval(timer);
                        }
                    },1000);
                    alert("Successfully send Captcha！");
                }else{
                    alert(res['message']);
                }
            }
        })
    });
}


// after all element are loaded
$(function () {
    bindCaptchaBtnClick();
});