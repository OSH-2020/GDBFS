// forcesimulation chart Part
// 新建一个力导向图
var NODE_SIZE = 30
var ARROW_SIZE = 7;
var BOARD_WIDTH = 5;
var forceSimulation;

function draw(nodes, edges) {
    forceSimulation = d3.forceSimulation()
        .force("link",d3.forceLink())
        .force("charge", d3.forceManyBody())
        .force("charge", d3.forceManyBody().strength(-700))
        .force("center",d3.forceCenter());
    var marge = {top:60,bottom:60,left:60,right:60}
    var svg = d3.select("svg")
    svg.append("g")
        .append("rect")
        .attr("x", BOARD_WIDTH)
        .attr("y", BOARD_WIDTH)
        .attr("width", 960-BOARD_WIDTH*2)
        .attr("height", 600-BOARD_WIDTH*2)
        .attr("fill", "white")
        .attr("strock", "red")
        .attr("style", `outline: ${BOARD_WIDTH}px solid grey;`) ;
    var width = svg.attr("width")
    var height = svg.attr("height")
    var g = svg.append("g")
        .attr("transform","translate("+marge.top+","+marge.left+")");
    // 设置一个color的颜色比例尺，为了让不同的nodes呈现不同的颜色
    /*var fillColorScale = d3.scaleOrdinal()
        .domain(d3.range(nodes.length))
        .range(d3.schemeCategory10);*/
    var fillColorScale = d3.scaleOrdinal()
        .domain(d3.range(2))
        .range(['LightSkyBlue', 'hotpink']);

    var strokeColorScale = d3.scaleOrdinal()
        .domain(d3.range(2))
        .range(['RoyalBlue  ', 'Crimson']);

    // 初始化力导向图，也就是传入数据
    // 转换节点数据
    forceSimulation.nodes(nodes)
        .on("tick",ticked);//这个函数很重要，后面给出具体实现和说明
    // 转换边数据
    forceSimulation.force("link")
        .links(edges)
        .distance(function(d){//每一边的长度
            return d.value*5*NODE_SIZE;
        })
    // 设置图形的中心位置
    forceSimulation.force("center")
        .x(width/2)
        .y(height/2);
    // 在浏览器的控制台输出
    console.log(nodes);
    console.log(edges);

    // 有了节点和边的数据后，我们开始绘制
    // marker's configuration
    var svg = d3.select("body").append("svg")
	    .attr("width", width)
	    .attr("height", height);

    svg.append("svg:defs").selectAll("marker")
        .data(["end"])      // Different link/path types can be defined here
        .enter().append("svg:marker")    // This section adds in the arrows
        .attr("id", 'arrow')
        .attr("markerUnits", "strokeWidth")
        .attr("viewBox", `0 ${-ARROW_SIZE} ${2*ARROW_SIZE} ${ARROW_SIZE*2}`)
        .attr("refX", NODE_SIZE+2*ARROW_SIZE)
        .attr("refY", 0)
        .attr("markerWidth", 2*ARROW_SIZE)
        .attr("markerHeight", ARROW_SIZE)
        .attr("orient", "auto")
        .append("svg:path")
        .attr("d", `M0,${-ARROW_SIZE} L${2*ARROW_SIZE},0 L0,${ARROW_SIZE}`)
        .attr("fill", "grey");

    // 绘制边
    var links = g.append("g")
        .selectAll("line")
        .data(edges)
        .enter()
        .append("line")
        .attr("stroke",function(d,i){
            return 'grey';
        })
        .attr("stroke-width",2)
        .attr("marker-end","url(#arrow)");
    var linksText = g.append("g")
        .selectAll("text")
        .data(edges)
        .enter()
        .append("text")
        .text(function(d){
            return d.relation;
        })

    // 绘制节点
    // 先为节点和节点上的文字分组
    var gs = g.selectAll(".circleText")
        .data(nodes)
        .enter()
        .append("g")
        .attr("transform",function(d,i){
            var cirX = d.x;
            var cirY = d.y;
            return "translate("+cirX+","+cirY+")";
        })
        .call(d3.drag()
            .on("start",started)
            .on("drag",dragged)
            .on("end",ended)
        );

    // 绘制节点
    gs.append("circle")
        .attr("r", NODE_SIZE)
        .attr("fill",function(d, i) {
            return fillColorScale(d['label']);
        })
        .attr("stroke", function(d, i) {
            return strokeColorScale(d['label']);
        })
        .attr("stroke-width", 3);
    // 文字
    // 以圆心为文本框左下角
    gs.append("text")
        .attr("x", -NODE_SIZE)
        .attr("y", 3)
        .text(function(d){
            return d.name;
        })

    // call functions
    function ticked(){
        links
            .attr("x1",function(d){return d.source.x;})
            .attr("y1",function(d){return d.source.y;})
            .attr("x2",function(d){return d.target.x;})
            .attr("y2",function(d){return d.target.y;})
            .attr("marker-end","url(#arrow)");

        linksText
            .attr("x",function(d){
            return (d.source.x+d.target.x)/2;
        })
        .attr("y",function(d){
            return (d.source.y+d.target.y)/2;
        });

        gs
            .attr('fill-opacity', 1)
            .attr("transform",function(d) {
                return "translate(" + d.x + "," + d.y + ")";
            });
    }

    function started(d){
        if(!d3.event.active){
            forceSimulation.alphaTarget(0.8).restart();
        }
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d){
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function ended(d){
        if(!d3.event.active){
            forceSimulation.alphaTarget(0);
        }
        // 表示最后不固定结点, 和neo4j browser的处理方式相反. 若要用neo4j的处理方式, 去掉这个即可
        d.fx = null;
        d.fy = null;
    }
}