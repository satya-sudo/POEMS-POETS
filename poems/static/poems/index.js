document.addEventListener('DOMContentLoaded',() =>{
    try {
        document.querySelector('#edit_profile').addEventListener('click',() => editProfile());
    } catch (err) {
        console.log(err);    
    }
    
    try {
        document.querySelector('#file').addEventListener('change',() => uplaodProfilePic());
        
    } catch (err) {
        console.log(err)
        
    }
    try {
        document.querySelector('#full-screen').addEventListener('click',() => fullscreentoggle());
    } catch (err) {
        console.log(err);
        
    }
    try{
        document.querySelector('#comment-toggle').addEventListener('click',() => commentbox());
    } catch (err){
        console.log(err)
    }
    try{
        document.querySelector('#comment-box-button').addEventListener('click',() => post_comment())
    } catch (err){
        console.log(err);
    }
    try{
        document.querySelector('#i_ur').addEventListener('click',() => add_to_libray())
    } catch (err){
        console.log(err);
    }
    try{
        document.querySelector('#n_ur').addEventListener('click',() => remove_from_libray())
    } catch (err){
        console.log(err);
    }
    try{
        document.querySelector('#d_ur').addEventListener('click',() => disabled_libray())
    } catch (err){
        console.log(err);
    }
})




function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

function commentbox(){
    comment_pannel = document.querySelector('#comment-box');
    x = document.querySelector('#comment-toggle');
    if (comment_pannel.style.display === 'block'){
        comment_pannel.style.display = 'none';
        x.innerHTML =  '<i class="fas fa-comments"></i>';
        
    }else{
        x.innerHTML =  '<i class="far fa-comments"></i>';
        comment_pannel.style.display = 'block';
    }

}


function add_to_libray(){
    let location_current = window.location.href;
    let pk = location_current.split('/')[4];
    
    fetch(location_current,{
        method: 'PUT',
        body: JSON.stringify({
            type: 'add_library',
            pk: pk
        }),
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });
    let s = document.querySelector('#i_ur');
    s.id = 'n_ur';
    s.innerHTML ='unLike'
    try{
        document.querySelector('#n_ur').addEventListener('click',() => remove_from_libray())
    } catch (err){
        console.log(err);
    }
}



function remove_from_libray(){
    let location_current = window.location.href;
    let pk = location_current.split('/')[4];
    
    fetch(location_current,{
        method: 'PUT',
        body: JSON.stringify({
            type: 'remove_library',
            pk: pk
        }),
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });
    let s = document.querySelector('#n_ur');
    s.id = 'i_ur';
    s.innerHTML = 'like'
    //setTimeout()
    try{
        document.querySelector('#i_ur').addEventListener('click',() => add_to_libray())
    } catch (err){
        console.log(err);
    }
}

function post_comment(){
    let comment =  document.querySelector('#comment-box-text-area').value
    let location_current = window.location.href;
    let pk = location_current.split('/')[4];
    if (comment.length != 0){
        fetch(location_current,{
            method: 'PUT',
            body: JSON.stringify({
                type: 'comment',
                pk: pk,
                comment:comment,
            }),
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        document.querySelector('#comment-box-text-area').value = '';
        let parent_div  = document.querySelector('#comment-box-text-area').parentElement;
        
        let new_comment = document.createElement('div');
        new_comment.className = "comment-div";
        let p = document.createElement('p');
        p.innerHTML = comment;
        let div_2 = document.createElement('div')
        div_2.innerHTML = 'Commented just now by YOU!';
        new_comment.append(p);
        new_comment.append(div_2);
        console.log(parent_div)
        parent_div.append(document.createElement('hr'))
        parent_div.append(new_comment)
    }else{
        pass
    }

}



function fullscreentoggle(){
    header_div = document.querySelector('#header');
    x = document.querySelector('#full-screen');
    if (header_div.style.display === 'flex' || header_div.style.display === 'inline-block'){
        header_div.style.display = 'none';
        x.innerHTML =  '<i class="fas fa-compress"></i>';
        
    }else{
        x.innerHTML =  '<i class="fas fa-expand"></i>';
        header_div.style.display = 'flex';
    }

}

function uplaodProfilePic(){
    file_div = document.querySelector('#file').parentElement
    let submit = document.createElement('input');
    submit.type = 'submit'
    submit.id = 'submit'

    submit.classList = 'hidden-stuff';

    let submit_label =document.createElement('label');
    submit_label.htmlFor = 'submit';
    submit_label.innerHTML = '<i class="fas fa-check"></i>';
    file_div.append(submit);
    file_div.append(submit_label);

    console.log(file_div.children)
}

function editProfile(){
    // parent element
    let parentdiv = document.querySelector('.profile_details');

    // getting its children
    let children = parentdiv.children;
    console.log(children);

    //getting old data
    let name_div = children[1];
    let about_div = children[2];
    let old_name = name_div.innerHTML;
    let old_about = about_div.innerHTML;

    // creating new nodes to replace the old
    let name_div_entry = document.createElement('input');
    name_div_entry.classList = 'inputarea';
    name_div_entry.type = 'text';
    name_div_entry.value = old_name;
    let about_div_entry = document.createElement('textarea');
    about_div_entry.classList = 'inputarea';
    about_div_entry.value = old_about;
    let save_button = document.createElement('input');
    save_button.classList = 'cus-button';
    save_button.id = 'save_edits';
    save_button.type = 'submit';
    save_button.value = 'save-profile';
   

    
    // replacing the old with new..
    parentdiv.replaceChild(name_div_entry,name_div);
    parentdiv.replaceChild(about_div_entry,about_div);
    parentdiv.replaceChild(save_button,children[3]);
    //parentdiv.replaceChild(label_for,children[4]);
    //parentdiv.append(save_button);
    

    // adding eventlistener to save_edit button
    try {
        document.querySelector('#save_edits').addEventListener('click',() => saveEdits());
    } catch (err) {
        console.log(err);
        
    }
}

function saveEdits(){

    event.preventDefault

    // parent element
    let parentdiv = document.querySelector('.profile_details');

    // getting its children
    let children = parentdiv.children;
    console.log(children);

    // getting pk for th user ...
    let location_current = window.location.href;
    let pk = location_current.split('/')[4];
    
    // getting the new details...
    let new_name = children[1].value;
    let new_about = children[2].value;

    console.log(new_name,new_about,pk);

    fetch(location_current,{
        method: 'PUT',
        body: JSON.stringify({
            type: 'edit-profile',
            pk: pk,
            name: new_name,
            about: new_about,
        }),
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });
    setTimeout(() => {location.reload();},600);

}

const navSlide = () => {
    const cus_burger = document.querySelector('.cus_burger');
    const nav = document.querySelector(".cus-nav-links");
    const navLinks = document.querySelectorAll('.cus-nav-links li');
    cus_burger.addEventListener('click',()=>{
        nav.classList.toggle('cus-nav-active');
        navLinks.forEach((link,index) => {
            if (link.style.animation){
                link.style.animation = ''
            }else{
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.5}s`;
                console.log(`navLinkFade 0.5s ease forwards ${index / 7 + 2}s`);
            }
        });
    });
    
}

navSlide()