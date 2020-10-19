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