
document.addEventListener('DOMContentLoaded', function() {

    editbtns = document.querySelectorAll(".editbtn");
    likebtns = document.querySelectorAll(".likebtn");

    editbtns.forEach((element) => {
        
        element.addEventListener('click', () => {
            edit(element);
        });
    });

    likebtns.forEach((element)=> {
        element.addEventListener('click', ()=>{
            like(element);
        });
    });

});

function like(element){
    post_id = element.dataset.id;
    console.log(post_id);

    form = new FormData();
    form.append("id", post_id);

    fetch("/like", {
        method: "POST",
        body: form
    })
    .then((response)=> response.json())
    .then((response) => {
        console.log(response);
        if (response.status == 201){

            if (response.liked == true){
                document.querySelector(`.likebtn[data-id="${post_id}"]`).innerHTML= "Unlike";
            }
            else{
                document.querySelector(`.likebtn[data-id="${post_id}"]`).innerHTML= "Like";
            }

            document.querySelector(`.like-count[data-id="${post_id}"]`).innerHTML = response.count;
        }
    })
    .catch(error =>{
        console.log('Error:', error);
    });
}

function edit(element) {
    post_id = element.dataset.id;
    console.log(post_id);

    posts_contents = document.querySelectorAll(".postcontent");
    console.log("posts_contents = "+posts_contents)

    for (let i= 0; i < posts_contents.length; i++) {
        if (posts_contents[i].dataset.id === post_id){
            post_content = posts_contents[i].textContent;
            var post_id = posts_contents[i].dataset.id
            
            console.log("post_content =" + post_content);

            textarea_content = 
            `<textarea class="form-control newcontent" rows="4" data-id="${post_id}" >${post_content}</textarea>`;

            document.querySelector(`.postcontent[data-id="${post_id}"]`).innerHTML= textarea_content

            document.querySelector(`.editbtn[data-id="${post_id}"]`).innerHTML= 
            `<i style="font-size:16px; color:#1CA345;" class="fa savebtn">&#xf0c7;</i>`;
        }
    }

    savebtns = document.querySelectorAll(".savebtn");
    savebtns.forEach((element) => {
        
        element.addEventListener('click', () => {
            newcontent = document.querySelector(`.newcontent[data-id="${post_id}"]`).value;
            save_edit(post_id, newcontent);
        });
    });

}

function save_edit(post_id, newcontent) {

    form = new FormData();
    form.append("id", post_id);
    form.append("content", newcontent);

    fetch("/edit", {
        method: "POST",
        body: form
    })
    .then((response)=>{
        document.querySelector(`.postcontent[data-id="${post_id}"]`).innerHTML = newcontent;
        document.querySelector(`.editbtn[data-id="${post_id}"]`).innerHTML= 
            `<i class="fa" style="font-size:18px;" >&#xf044;</i>`;

    })
    .catch(error =>{
        console.log('Error:', error);
    });
}