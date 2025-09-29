let format_mode = 0;
const format_options = document.querySelector(".option_slider a:nth-child(3)");
// console.log(format_options.length);
function move_header() {
    // document.getElementById("splash").style.left = "-100%";
    document.getElementById("splash").style.opacity = "0%";
    document.getElementById("content_container").style.opacity = "100%";
    // document.getElementById("splash").style.zIndex = "-1";
    setTimeout(() => {
        document.getElementById("splash").style.zIndex = "-1";
        
    }, 500);  
    document.getElementById("whole").style.overflow = "initial";
}

function update_format_slider() {
    if (format_mode == 0) {
        document.getElementById("format_bubble").style.left = "52%";
        document.querySelector(".option_slider a:nth-child(2)").style.color = "rgb(117, 117, 117)";
        document.querySelector(".option_slider a:nth-child(3)").style.color = "white";
        format_mode = 1;
    }
    else {
        document.getElementById("format_bubble").style.left = "3%";
        document.querySelector(".option_slider a:nth-child(2)").style.color = "white";
        document.querySelector(".option_slider a:nth-child(3)").style.color = "rgb(117, 117, 117)";
        format_mode = 0;
    }

    
}

document.getElementById("search_button").addEventListener("click", async () => {
    const query = document.getElementById("input_bar").value.trim();
    if (query == "") {
        return;
    }

    const response = await fetch("/search", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ query })
    });
    
    const data = await response.json();

    const discogsDiv = document.getElementById("Discogs");
    discogsDiv.innerHTML = "";
    const shop_title = document.createElement("h1");
    shop_title.classList.add("montserrat-light");
    shop_title.innerText = "Data from Discogs:";
    discogsDiv.appendChild(shop_title);


    const ebayDiv = document.getElementById("Ebay");
    ebayDiv.innerHTML = "";
    const shop_title2 = document.createElement("h1");
    shop_title2.classList.add("montserrat-light");
    shop_title2.innerText = "Data from eBay:";
    ebayDiv.appendChild(shop_title2);
    


    // Adding discogs data to the web as divs
    data.discogs.forEach(item => {
        const card = document.createElement("div");
        card.classList.add("result_card");

        const prod_details = document.createElement("div");
        prod_details.classList.add("product_details");

        const disclaimer = document.createElement("h3");
        disclaimer.textContent = "Data provided by Discogs.";

        const img_holder = document.createElement("div");
        img_holder.classList.add("image_holder");
        
        if (item.thumb != null) {
            img_holder.style.backgroundImage = 'url("' + item.thumb + '")';
        }
        else {
            img_holder.innerHTML = "&#9835;";
        }
        
        

        const title = document.createElement("h3");
        title.textContent = item.title;

        const artist = document.createElement("h4");
        artist.textContent = item.artist;

        const release = document.createElement("p");
        release.textContent = item.released;

        const format = document.createElement("p");
        format.textContent = item.format;

        const price = document.createElement("a");
        price.textContent = "Shop on Discogs starting at: $" + item.lowest_price;
        price.href = item.address;

        if (title != null) {
            prod_details.appendChild(title);
        }
        prod_details.appendChild(artist);
        prod_details.appendChild(release);
        prod_details.appendChild(format);
        prod_details.appendChild(price);
        prod_details.appendChild(disclaimer);

        card.appendChild(img_holder);
        card.appendChild(prod_details);
        discogsDiv.appendChild(card);
    });

    // Adding ebay data to the web as divs
    data.ebay.forEach(item => {
        const card = document.createElement("div");
        card.classList.add("result_card");

        const prod_details = document.createElement("div");
        prod_details.classList.add("product_details");

        const img_holder = document.createElement("div");
        img_holder.classList.add("image_holder");
        
        const disclaimer = document.createElement("h3");
        disclaimer.textContent = "Data provided by eBay.";

        if (item.thumb != null) {
            img_holder.style.backgroundImage = 'url("' + item.thumb + '")';
        }
        else {
            img_holder.innerHTML = "&#9835;";
        }
        
        

        const title = document.createElement("h3");
        title.textContent = item.title;

        const seller = document.createElement("h4");
        seller.textContent = "Seller: " + item.seller.username + " (" + item.seller.feedbackPercentage + "%)";

        const price = document.createElement("a");
        price.textContent = "Shop on eBay: $" + item.price;
        price.href = item.address;

        prod_details.appendChild(title);
        prod_details.appendChild(seller);
        prod_details.appendChild(price);
        prod_details.appendChild(disclaimer);

        card.appendChild(img_holder);
        card.appendChild(prod_details);
        ebayDiv.appendChild(card);
    });

});

document.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch("/picks", {
        method: "GET"
    });

    const picks_data = await response.json();

    const targetDiv = document.getElementById("week_picks");

    console.log(picks_data);
    picks_data.discogs.forEach(item => {
        const card = document.createElement("div");
        card.classList.add("result_card");

        const img_holder = document.createElement("div");
        img_holder.classList.add("small_image_holder");
        if (item.thumb != null) {
            img_holder.style.backgroundImage = 'url("' + item.thumb + '")';
        }
        else {
            img_holder.innerHTML = "&#9835;";
        }
        
        const prod_details = document.createElement("div");
        prod_details.classList.add("product_details");

        const title = document.createElement("h3");
        title.textContent = item.title;

        const artist = document.createElement("h4");
        artist.textContent = item.artist;

        const release = document.createElement("p");
        release.textContent = item.released;

        const price = document.createElement("a");
        if (item.lowest_price != null) {
            price.textContent = "Shop on Discogs starting at: $" + item.lowest_price;
        }
        else {
            price.textContent = "View on Discogs";
            price.style.backgroundColor = "grey";
        }
        price.href = item.address;

        const disclaimer = document.createElement("h3");
        disclaimer.textContent = "Data provided by Discogs.";

        prod_details.appendChild(title);
        prod_details.appendChild(artist);
        prod_details.appendChild(release);
        prod_details.appendChild(price);
        prod_details.appendChild(disclaimer);

        card.appendChild(img_holder);
        card.appendChild(prod_details);

        targetDiv.appendChild(card);
    });
});
