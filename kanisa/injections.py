def wait_4_order(driver):
    driver.execute_script('''
        const targetNode = document.getElementById('available_orders_list_container');
        const config = {
            attributes: true,
            childList: true,
            subtree: true
        };
        const callback = function(mutationsList, observer) {
            for (let mutation of mutationsList) {
                console.log(mutation)
                if (mutation.type === 'childList') {
                    if (mutation.addedNodes.length > 0) {
                        if (typeof(mutation.addedNodes[0]) === 'object') {
                            try {
                                order = mutation.addedNodes[0]
                                orderID = order.getAttribute('data-id')
                                window.open(`https://essayshark.com/writer/orders/${orderID}.html`, '_blank', 'height=100,width=100,toolbar=0,location=0,menubar=0')
                            } catch (TypeError) {
                                continue
                            }
                        }
                    }
                }
            }
        };
        const observer = new MutationObserver(callback);
        observer.observe(targetNode, config);
    ''')


def ping_timeout_and_submit_bid(driver):
    driver.execute_script('''
        var time_checker = setInterval(function() { ping(); }, 700);
        var ping = function() {
            $.ajax({
                url: "/writer/orders/ping.html",
                type: 'GET',
                data: {
                  order: w3tVar('order_id'),
                },
                success: function(data) {
                    checkStatus(data);
                },
            });
        };
        var checkStatus = function (data) {
          console.log(data);
          if (data.read_time_remain == 10 && data.pr==1){
           clearInterval(time_checker);
           jQuery("#id_order_bidding_form").submit();
          }else if (data.read_time_remain == 0 && jQuery("#btn_cancel_this_order_3").length != 1){
           clearInterval(time_checker);
           jQuery("#id_order_bidding_form").submit();
          }
        }
    ''')


def process_bid(driver):
    driver.execute_script('''
        var process = function () {
          console.log("processing form data ...")
          var bidInputEl = $("#id_bid");
          var bidForm = $("#id_order_bidding_form");
          var submitBtn = $("#apply_order");
          bidInputEl.val(-10)
          submitBtn.click()
          minBid = $("#id_bid-error").text().split("$")[1]
          if (minBid < 5) {
            minBid = 5
          }
          bidInputEl.val(minBid)
          $("#apply_order").click()
        }
        process()
    ''')


def dowload_files(driver):
    driver.execute_script('''
        var downloadFiles = function () {
          console.log("downloading files...")
          var files = $("[data-orig-file-name]")
          for (var i = files.length - 1; i >= 0; i--) {
            files[i].click();
          }
        }
        downloadFiles()
    ''')


def check_conditions(driver, config):
    script = '''
        var config = {0};
        {1}
    '''.format(
        config,
        '''
            var serviceType = document.getElementsByClassName("order-id")[0].getAttribute("data-title")
            var numPages = parseInt(document.getElementsByClassName("pages_need bold tooltip_n")[0].innerText)
            var customerStatus = document.getElementsByClassName("ustatus_label")[0].innerText
            var customerRating = parseFloat(document.getElementsByClassName("rating_view")[0].getAttribute("data-rating"))
            var discardBtn = document.getElementsByClassName("discard")[0]
            var deadlineEl = document.getElementsByClassName("d-date")[0]
            var deadline = moment(deadlineEl.innerText, "MMM D, YYYY at hh:mm A") // eg May 5, 2020 at 7:00 PM
            var deadlineLB = moment().add(config.minDeadline, "hours")
            var deadlineUB = moment().add(config.maxDeadline, "hours")
            var checkConditions =  function () {
                console.log("checking conditions to discard order...")
                if (config.discard_offline_customers && customerStatus === "OFFLINE") {
                    console.log("discarding order...")
                    discardBtn.click()
                    return
                }
                if (numPages < config.min_pages || numPages > config.max_pages ) {
                    console.log("discarding order...")
                    discardBtn.click()
                    return
                }
                if (config.discard_editing_or_rewriting && serviceType === "Editing or rewriting") {
                    console.log("discarding order...")
                    discardBtn.click()
                    return
                }
                if (config.dicard_assignments && serviceType.toLocaleLowerCase() === "assignment") {
                    console.log("discarding order...")
                    discardBtn.click()
                    return
                }
                if (customerRating < config.min_customer_rating) {
                    console.log("discarding order...")
                    discardBtn.click()
                    return
                }
                if (!deadline.isAfter(deadlineLB)){
                    console.log("discarding order...")
                    discardBtn.click()
                    return
                }if (config.discard_orders_with_client_contacts) {
                    //pass
                }
            }
            checkConditions()
        '''
    )
    driver.execute_script(script)
