function imgError(image) {
    image.onerror = "";
    image.src = "/static/missing.png";
    return true;
}

document.addEventListener("DOMContentLoaded", function(){
    Plotly.plot('national_chart',national, {});a
});

document.addEventListener("DOMContentLoaded", function(){


    Plotly.plot('temp_chart',temperature, {});
    Plotly.plot('carbon_chart',carbon, {});
    Plotly.plot('sea_ice_chart',sea_ice, {});


});

