// function buildPlot() {
//     /* data route */
//   var url = "/api/maps";
//   d3.json({{data}}, function(response) {
  	
//     console.log(response);

//     var data = [response];

//     var layout = {
//       title: "Pet Pals",
//       xaxis: {
//         title: "Pet Type"
//       },
//       yaxis: {
//         title: "Number of Pals"
//       }
//     };

//     Plotly.newPlot("plot", data, layout);
//   });
// }

// buildPlot();

function buildCharts() {
	var url = "/api/charts";
    d3.json(url).then(function (data) {

            var migrants = data.map(d => d.migrants);
            var countries = data.map(d => d.labels1);
            var labels_to_from = data.map(d => `destination: ${d.labels1[0]} + origin: ${d.labels1[1]}`);
            
            var pieData = [
                {
                    values: migrants,
                    labels: labels_to_from,
                    hovertext: countries,
                    hoverinfo: "hovertext",
                    type: "pie"
                }
            ];

            var pieLayout = {
                title: "Top 10 Origins",
            };

            Plotly.plot("pie_top", pieData, pieLayout);
        });
}
function buildBottom10(data) {
    d3.json("../static/data/top_10_dest.json").then(function (data) {

            var migrants = data.map(d => d.Total);
            var country = data.map(d => d.Destination);
            
            var pieData = [
                {
                    values: migrants,
                    labels: country,
                    hovertext: migrants,
                    hoverinfo: "hovertext",
                    type: "pie"
                }
            ];

            var pieLayout = {
                title: "Top 10 Destinations",
            };

            Plotly.plot("pie_bottom", pieData, pieLayout);
        });
}
buildCharts();
buildBottom10();