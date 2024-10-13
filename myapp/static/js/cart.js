// var updateBtns = document.getElementsByClassName('update-cart')

// for(var i = 0; i < updateBtns.length; i++){
//     updateBtns[i].addEventListener('click',function(){
//         var productId = this.dataset.product
//         var action = this.dataset.action
//         console.log('productId:',productId,'action:',action)

//         console.log('USER:',user)
//         if(user === 'AnonymousUser'){
//             console.log('Not logged in')
//         }else{
//             console.log('USer is logged in, sentingdata..')
//         }
//             updateUserOrder(productId, action)
//     })
// }


// function updateUserOrder(productId, action){
// 	console.log('User is authenticated, sending data...')

// 		var url = 'update_item'

// 		fetch(url, {
// 			method:'POST',
// 			headers:{
// 				'Content-Type':'application/json',
// 				'X-CSRFToken':csrftoken,
// 			}, 
// 			body:JSON.stringify({'productId':productId, 'action':action})
// 		})
// 		.then((response) => {
// 		   return response.json();
// 		})
// 		.then((data) => {
// 		    // location.reload()
//             console.log('data:',data)
// 		});
// }
///////////////////////////////////

document.addEventListener('DOMContentLoaded', function() {
    var updateBtns = document.getElementsByClassName('update-cart');
    for (var i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function(event) {
            event.preventDefault();
            var productId = this.dataset.product;
            var action = this.dataset.action;

            console.log('productId:', productId, 'action:', action);

            console.log('USER:', user);
            if (user === 'AnonymousUser') {
                console.log('Not logged in');
            } else {
                console.log('User is logged in, sending data..');
                updateUserOrder(productId, action);
            }
        });
    }
});

// function updateUserOrder(productId, action) {
//     console.log('User is authenticated, sending data...');

//     var url = 'update_item';

//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken,
//         },
//         body: JSON.stringify({ 'productId': productId, 'action': action })
//     })
//     .then((response) => response.json())
//     .then((data) => {
//         console.log('data:', data);
//         // รีเฟรชหน้าหลังจากอัปเดต
//         location.reload(); // เพิ่มบรรทัดนี้เพื่อรีเฟรชหน้า
//     });

    
// }

function updateUserOrder(productId, action) {
    console.log('Sending data:', {'productId': productId, 'action': action}); // ตรวจสอบค่าที่ส่งไป

    fetch('/update_item', { // ตรวจสอบ URL ให้ถูกต้อง
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('data:', data);
        // location.reload(); // รีเฟรชหน้าหลังจากอัปเดต
    });
}

function updateCartItem(productId, action) {
    var quantityElement = document.querySelector(`a[data-product="${productId}"]`).closest('tr').querySelector('.quantity');
    var currentQuantity = parseInt(quantityElement.textContent);
    
    // อัปเดตจำนวนสินค้าตาม action
    if (action === 'add') {
        quantityElement.textContent = currentQuantity + 1;
    } else if (action === 'remove') {
        if (currentQuantity > 0) {
            quantityElement.textContent = currentQuantity - 1;
        }
    }
}






////////////////////////

