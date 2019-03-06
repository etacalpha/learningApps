//                      SETUP CANVAS, SVG, GROUPS
//************************************************************************/
//
// get div by class and append a svg element
const svg = d3.select('.canvas')
    .append('svg')
    .attr('width', 600)
    .attr('height', 600);

// create margins and dimensions
const margin = {
    top: 20,
    right: 20,
    bottom: 100,
    left: 100
}

// define graph width and height
const graphWidth = 600 - margin.left - margin.right;
const graphHeight = 600 - margin.top - margin.bottom;

//create graph group
const graph = svg.append('g')
    .attr('width', graphWidth)
    .attr('height', graphHeight)
    .attr('transform', `translate(${margin.left},${margin.top})`);

//create x and y axis groups
const xAxisGroup = graph.append('g')
    .attr('transform', `translate(0, ${graphHeight})`);
const yAxisGroup = graph.append('g');

//scales

//create d3 linear Scale
const y = d3.scaleLinear()
    .range([graphHeight, 0]);

// create d3 band scale
const x = d3.scaleBand()
    .range([0, 500])
    .paddingInner(0.2)
    .paddingOuter(0.2);

//create the axes
const xAxis = d3.axisBottom(x);

const yAxis = d3.axisLeft(y)
    .ticks(3)
    .tickFormat(d => d + ' orders');

//transitions
const t = d3.transition().duration(1500);


//
//***************************************************************************/
//


/**
 * This gets data from data base and updates scales, joins to 
 * graph group, removes unused shapes, adds shapes as needed.
 * @param {*} data 
 */
const update = (data) => {

    // find min and max of data
    // const min = d3.min(data, d => d.orders); get min value from data
    // const extenet = d3.extent(data, d => d.orders); get min/max value from data
    const max = d3.max(data, d => d.orders); // get max value from data


    //update d3 linear/band scales domain
    y.domain([0, max]); // sets domain(the range of values in data) for y(height)
    x.domain(data.map(item => item.name)); // sets domain for width based on data name

    //create rect and join data to graph group
    const rects = graph.selectAll('rect')
        .data(data);

    //remove exit selection
    rects.exit().remove();

    // updates current shapes in DOM
    rects.attr('width', x.bandwidth)
        .attr('fill', 'orange')
        .attr('x', d => x(d.name))

    // adds rects as needed
    rects.enter()
        .append('rect')
        // .attr('width', 0) starting point given in the tween
        .attr('height', 0)
        .attr('fill', 'orange')
        .attr('x', d => x(d.name))
        .attr('y', graphHeight)
        .merge(rects) // merges incoming with exsisting
        .transition(t)
        .attrTween('width', widthTween)
        .attr('y', d => y(d.orders))
        .attr('height', d => graphHeight - y(d.orders))

    // Call axes
    xAxisGroup.call(xAxis);
    yAxisGroup.call(yAxis);

    // update x axis text
    xAxisGroup.selectAll('text')
        .attr('transform', 'rotate(-50)')
        .attr('text-anchor', 'end')

}


//get data from JSON
/**     d3.json('/JSON/menu.json').then(data =>{});*/

// get data from firestore db by getting the collection and using get request
/**     db.collection('dishes').get().then(res => {
        var data = [];
        res.docs.forEach(doc => {
            data.push(doc.data());
        });
        update(data);
    }); 
*/

var data = [];
// Get data/changes to data from db
db.collection('dishes').onSnapshot(res => {
    res.docChanges().forEach(change => {
        const doc = {
            ...change.doc.data(),
            id: change.doc.id
        };
        switch (change.type) {
            case 'added':
                data.push(doc);
                break;
            case 'modified':
                const index = data.findIndex(item => item.id == doc.id);
                data[index] = doc;
                break;
            case 'removed':
                data = data.filter(item => itemd.id !== doc.id);
                break;
            default:
                break;
        }
    });
    update(data);
})

// TWEENS
const widthTween = (d) => {

    //define interpolation
    // d3.inerpolation returns a function which we call "i"
    let i = d3.interpolate(0, x.bandwidth());

    // return a function whick takes in a time ticker 't'
    return function (t) {

        // return the value from passing the ticker into the interpolation
        return i(t);
    }
}