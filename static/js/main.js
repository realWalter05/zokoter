
function GetOpponentData() {
    console.log("Getting opponent data js");
    $.ajax({
        data : {},
        type : 'POST',
        url : "/opponent",
    })
    .done(function(data) {
        console.log(data.combinations);

        let combinations = data.combinations;
        let combinations_elements = "";
        
        combinations_elements += "High card: ";
        if (combinations.includes("High card")) {
             combinations_elements += "<b>Yes</b>";
        } else {
            combinations_elements += "<em>No</em>";
        }

        combinations_elements += " Pair: ";
        if (combinations.includes("Pair")) {
             combinations_elements += "<b>Yes</b>";
        } else {
            combinations_elements += "<em>No</em>";
        }
        
        combinations_elements += "Two pair: ";
        if (combinations.includes("Two pair")) {
             combinations_elements += "<b>Yes</b>";
        } else {
            combinations_elements += "<em>No</em>";
        }    

        combinations_elements += " Three of a kind: ";
        if (combinations.includes("Three of a kind")) {
             combinations_elements += "<b>Yes</b>";
        } else {
            combinations_elements += "<em>No</em>";
        }   
        
        combinations_elements += " Straight: ";
        if (combinations.includes("Straight")) {
             combinations_elements += "<b>Yes</b>";
        } else {
            combinations_elements += "<em>No</em>";
        }   
        
        combinations_elements += " Flush: ";
        if (combinations.includes("Flush")) {
             combinations_elements += "<b>Yes</b>";
        } else {
            combinations_elements += "<em>No</em>";
        }   
        
        combinations_elements += " Full house: ";
        if (combinations.includes("Full house")) {
             combinations_elements += "<b>Yes</b>";
        } else {
            combinations_elements += "<em>No</em>";
        }      
        
        combinations_elements += " Four of a kind: ";
        if (combinations.includes("Four of a kind")) {
             combinations_elements += "<b>Yes</b>";
        } else {
            combinations_elements += "<em>No</em>";
        } 
        
        combinations_elements += " Straight flush: ";
        if (combinations.includes("Straight flush")) {
             combinations_elements += "<b>Yes</b>";
        } else {
            combinations_elements += "<em>No</em>";
        } 
        
        combinations_elements += " Royal flush: ";
        if (combinations.includes("Royal flush")) {
             combinations_elements += "<b>Yes</b>";
        } else {
            combinations_elements += "<em>No</em>";
        }         
        
        let combinations_div = document.getElementById("opponent-combinations");
        combinations_div.innerHTML = combinations_elements;

        document.getElementById("opponent-best-odds").insertAdjacentText('beforeend', data.best_odds.toString());
        document.getElementById("opponent-best-cards").insertAdjacentText('beforeend', data.best_cards);
        document.getElementById("opponent-better-odds-chance").insertAdjacentText('beforeend', data.better_odds);

        document.getElementById("opponent-odds-details").insertAdjacentText('afterbegin', data.lower_odds_count);
        document.getElementById("opponent-odds-details").insertAdjacentText('beforeend', data.all_odds_count);
        
        if (JSON.parse(data.winnable)) {
            document.getElementById("opponent-winnable").insertAdjacentText('beforeend', "Winnable");
        } else {
            document.getElementById("opponent-winnable").insertAdjacentText('beforeend', "<b>Unwinnable</b>");
        }
        
        document.getElementById("opponent-table-position").insertAdjacentText('beforeend', data.table_position);
    })
}
