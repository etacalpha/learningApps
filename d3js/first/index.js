// select svg container
const svg = d3.select('svg');

d3.json('/JSON/planets.json').then(data => {

    const circs = svg.selectAll('circle')
        .data(data);

    //add attr to circs already present in DOM
    circs.attr('cy', 200)
        .attr('cx', d => d.distance)
        .attr('fill', d => d.fill)
        .attr('r', d => d.radius)

    //append the enter selection to the DOM
    circs.enter()
        .append('circle')
        .attr('cy', 200)
        .attr('cx', d => d.distance)
        .attr('fill', d => d.fill)
        .attr('r', d => d.radius);
})