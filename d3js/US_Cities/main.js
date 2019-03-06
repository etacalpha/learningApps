//Width and height of map
var width = 960;
var height = 500;

// D3 Projection
var projection = d3.geoAlbersUsa()
    .translate([width / 2, height / 2])    // translate to center of screen
    .scale([1100]);                       // scale things down so see entire US

// Define path generator
var path = d3.geoPath()        // path generator that will convert GeoJSON to SVG paths
    .projection(projection);  // tell path generator to use albersUsa projection

//Create SVG element and append map to the SVG
var svg = d3.select("#map-holder")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .call(d3.zoom().on("zoom", function () {
        svg.attr("transform", d3.event.transform)
    }))
    .append("g");

// Load GeoJSON data and merge with states data
d3.json("us-states.json", function (json) {

    // Bind the data to the SVG and create one path per GeoJSON feature
    svg.selectAll("path")
        .data(json.features)
        .enter()
        .append("path")
        .attr("d", path)
        .style("stroke", "#000")
        .style("stroke-width", "3")
        .style("fill", "rgb(213,222,217)")
});

//get data from Cities.json and create
d3.json("Cities.json", function (places) {
    var g = svg.selectAll(null)
        .data(places)
        .enter()
        .append("g")
        .attr("transform", function (d) {
            return "translate(" + projection([
                d.Location.split(", ").map(Number)[0],
                d.Location.split(", ").map(Number)[1]
            ]) + ")";
        });

    // -1- Create a tooltip div that is hidden by default:
    var tooltip = d3.select("#map-holder")
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("background-color", "black")
        .style("width","300px")
        .style("heigth","300px")
        .style("border-radius", "15px")
        .style("padding", "10px")
        .style("color", "white")

    // -2- Create 3 functions to show / update (when mouse move but stay on same circle) / hide the tooltip
    var showTooltip = function (d) {
        tooltip
            .transition()
            .duration(200)
        tooltip
            .style("opacity", 1)
            .html("City: " + d.City +"\n"+ "County: " + d.County)
            .style("left", (d3.mouse(this)[0] + 30) + "px")
            .style("top", (d3.mouse(this)[1] + 30) + "px")
    }

    // function to move tooltip
    var moveTooltip = function (d) {
        tooltip
            .style("left", (d3.mouse(this)[0] + 30) + "px")
            .style("top", (d3.mouse(this)[1] + 30) + "px")
    }

    //function to hide tooltip
    var hideTooltip = function (d) {
        tooltip
            .transition()
            .duration(200)
            .style("opacity", 0)
    }

    // add circles to group
    g.append("circle")
        .attr("r", .5)
        .attr("fill", "blue")
        .on("mouseover", showTooltip)
        .on("mousemove", moveTooltip)
        .on("mouseout", hideTooltip);

});

