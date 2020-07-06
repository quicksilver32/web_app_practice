fetch('/json_dashboard', {method: 'POST'}).then(res => res.json()).then(function (data) {  //фуункция получения json
//    console.log(data)

    for (key in data['objects']) {
        var sel = document.getElementById('address')
        var opt = document.createElement('option')
        if (data['objects'][key]['flat'] == null) {
            var room = '';
        } else {
            room = ', кв. ' + data['objects'][key]['flat']
        }
        opt.innerHTML = data['objects'][key]['address'] + room;
        sel.appendChild(opt);
    }
// ГИСТОРГРАММА ПО ПОТРЕБЛЕНИЮ ДОМОВ ЗА ОПР ПЕРИОД
//    var d3data = []
//    for (key in data['data']){
//        d3data.push(data['data'][key])
//    }
//    console.log(d3data)
//    var count_data = []
//    var count = 0
//    for (key in data['data']){
//        count_data.push(count)
//        count++
//    }
//
//    var height = 300,
//        width = 1700,
//        margin = 50
//
//    var xAxisLength = width - 2 * margin;
//    var yAxisLength = height - 2 * margin;
//
//    var xScale = d3.scale.ordinal()
//        .rangeRoundBands([0, xAxisLength + margin], .1)
//        .domain(d3data.map(function(d) { return d.address; }));
//
//    var yScale = d3.scale.linear()
//        .domain([
//                d3.min(d3data, function(d) { return d.сonsumption; }),
//                d3.max(d3data, function(d) { return d.сonsumption + 1 / 2 * d.сonsumption; })
//        ]).range([yAxisLength, 0]);
//
//    var svg = d3.select("body").append("svg")
//        .attr("class", "axis")
//        .attr("width", width)
//        .attr("height", height);
//
//    var xAxis = d3.svg.axis()
//            .scale(xScale)
//            .orient("bottom");
//
//    var yAxis = d3.svg.axis()
//             .scale(yScale)
//             .orient("left");
//
//    svg.append("g")
//        .attr("class", "x-axis")
//        .attr("transform",
//         "translate(" + margin + "," + (height - margin) + ")")
//        .call(xAxis)
//            .selectAll("text")
////            .style("text-anchor", "middle")
////            .style("font-weight", "bolder")
////            .attr("font-size", "10px")
////            .attr("transform", "rotate(3)")
//            .attr("class", "text")
//            .attr("style", "opacity: 0");
//
//    svg.append("g")
//        .attr("class", "y-axis")
//        .attr("transform",
//            "translate(" + margin + "," + margin + ")")
//        .call(yAxis);
//
//    d3.selectAll("g.y-axis g.tick")
//        .append("line")
//        .classed("grid-line", true)
//        .attr("x1", 0)
//        .attr("y1", 0)
//        .attr("x2", xAxisLength)
//        .attr("y2", 0);
//
//    svg.append("g")
//        .attr("transform",  // сдвиг оси вправо
//             "translate(" + margin + ", 0)")
//        .selectAll(".bar")
//        .data(d3data)
//        .enter().append("rect")
//        .attr("class", "bar")
//        .attr("x", function(d) { return xScale(d.address); })
//        .attr("width", xScale.rangeBand())
//        .attr("y", function(d) { return yScale(d.сonsumption); })
//        .attr("height", function(d) { return height - yScale(d.сonsumption) - margin; })
//        .attr("fill", "rgb(0, 255, 127)");
//
//    svg.selectAll(".bar")
//        .data(count_data)
//        .attr("id", function(d) { return d;});
//
//    svg.selectAll(".text")
//        .data(count_data)
//        .attr("id", function(d) { return (d + "text");});
//
//    $(".bar")
//        .mouseenter(function(e) {
//        var id = e.target.id;
//        console.log(id)
//        $("#" + id + "text").attr("style", "opacity: 1; font-weight:bold; text-anchor:middle")
//             // навели курсор на объект (не учитываются переходы внутри элемента)
//    })
//        .mouseleave(function(e){
//        var id = e.target.id;
//        console.log(id)
//        $("#" + id + "text").attr("style", "opacity: 0")
//            // отвели курсор с объекта (не учитываются переходы внутри элемента)
//    });

// ГРФИК ПО ПОТРЕБЛЕНИЮ 1 ДОМА ЗА ПЕРИОД ПО ДНЯМ
//    var d3data = []
//    for (key in data['data']){
//        d3data.push(data['data'][key])
//    }
//    console.log(d3data)
//
//
//    var count_data = []
//    var count = 0
//    for (key in data['data']){
//        count_data.push(count)
//        count++
//    }
//
//    var height = 300,
//        width = 1700,
//        margin = 50
//
//    var xAxisLength = width - 2 * margin;
//    var yAxisLength = height - 2 * margin;
//
//    var xScale = d3.scale.ordinal()
//        .rangeRoundBands([0, xAxisLength + margin])
//        .domain(d3data.map(function(d) { return d.dt; }));
//
//    var yScale = d3.scale.linear()
//        .domain([
//                d3.min(d3data, function(d) { return d.сonsumption; }),
//                d3.max(d3data, function(d) { return d.сonsumption + 1 / 2 * d.сonsumption; })
//        ]).range([yAxisLength, 0]);
//
//    var svg = d3.select("body").append("svg")
//        .attr("class", "axis")
//        .attr("width", width)
//        .attr("height", height);
//
//    var xAxis = d3.svg.axis()
//            .scale(xScale)
//            .orient("bottom");
//
//    var yAxis = d3.svg.axis()
//             .scale(yScale)
//             .orient("left");
//
//    svg.append("g")
//        .attr("class", "x-axis")
//        .attr("transform",
//         "translate(" + margin + "," + (height - margin) + ")")
//        .call(xAxis)
//            .selectAll("text")
//////            .style("text-anchor", "middle")
//////            .style("font-weight", "bolder")
//////            .attr("font-size", "10px")
//////            .attr("transform", "rotate(3)")
//            .attr("class", "text")
//            .attr("style", "opacity: 0");
//
//    svg.append("g")
//        .attr("class", "y-axis")
//        .attr("transform",
//            "translate(" + margin + "," + margin + ")")
//        .call(yAxis);
//
//    d3.selectAll("g.x-axis g.tick")
//        .append("line") // добавляем линию
//        .classed("grid-line", true) // добавляем класс
//        .attr("x1", 0)
//        .attr("y1", 0)
//        .attr("x2", 0)
//        .attr("y2", - (height - 2 * margin));
//
//    d3.selectAll("g.y-axis g.tick")
//        .append("line")
//        .classed("grid-line", true)
//        .attr("x1", 0)
//        .attr("y1", 0)
//        .attr("x2", xAxisLength + margin)
//        .attr("y2", 0);
//
//    var line = d3.svg.line()
//            .x(function(d){return xScale(d.dt) + 1.5*margin;})
//            .y(function(d){return yScale(d.сonsumption)+margin;});
//
//    svg.append("g").append("path")
//        .attr("d", line(d3data))
//        .style("stroke", "steelblue")
//        .style("stroke-width", 2);
//
//    svg.selectAll(".dot")
//        .data(d3data)
//        .enter().append("circle")
//        .attr("class", "dot")
//        .attr("r", 3.5)
//        .attr("cx", function(d) { return xScale(d.dt)+ 1.5*margin; })
//        .attr("cy", function(d) { return yScale(d.сonsumption) + margin; });
//
//    svg.selectAll(".dot")
//        .data(count_data)
//        .attr("id", function(d) { return d;});
//
//    svg.selectAll(".text")
//        .data(count_data)
//        .attr("id", function(d) { return (d + "text");});
//
//    $(".dot")
//        .mouseenter(function(e) {
//        var id = e.target.id;
//        console.log(id)
//        $("#" + id + "text").attr("style", "opacity: 1; font-weight:bold; text-anchor:middle")
//             // навели курсор на объект (не учитываются переходы внутри элемента)
//    })
//        .mouseleave(function(e){
//        var id = e.target.id;
//        console.log(id)
//        $("#" + id + "text").attr("style", "opacity: 0")
//            // отвели курсор с объекта (не учитываются переходы внутри элемента)
//    });
});