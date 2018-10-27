function buildTop10() {
    d3.json("../static/data/top_10_origin.json").then(function (data) {

            var migrants = data.map(d => d.Total);
            var country = data.map(d => d.Origin);
            
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
                title: "Top 10 Origins",
            };

            Plotly.plot("pie_top", pieData, pieLayout);
        });
    // d3.json("../static/data/top_10.json").then(function (data) {

    //         var migrants = data.map(d => d.migrants);
    //         var countries = data.map(d => d.labels1[1]);
    //         var labels_to_from = data.map(d => `destination: ${d.labels1[0]} + origin: ${d.labels1[1]}`);
            
    //         var pieData = [
    //             {
    //                 values: migrants,
    //                 labels: countries   ,
    //                 hovertext: countries,
    //                 hoverinfo: "hovertext",
    //                 type: "pie"
    //             }
    //         ];

    //         var pieLayout = {
    //             title: "Top 10 Origins",
    //         };

    //         Plotly.plot("pie_top", pieData, pieLayout);
    //     });
}
function buildBottom10(data) {
    d3.json("../static/data/top_10_dest.json").then(function (data) {
            // console.log(data)
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
buildTop10();
buildBottom10();