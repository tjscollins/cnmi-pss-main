(ns cnmipss.handlers.api
  (:require [re-frame.core :as rf]
            [klang.core :refer-macros [info!]]))

(defn subscribed [pns]
  (fn [[ok res :as response]]
    (info! "Subscribed: " ok res response)
    (let [jq js/jQuery]
      (if ok
        (do
          (rf/dispatch [:subscribed pns])
          (rf/dispatch [:subscription-error nil]))
        (let [message (-> res
                          clojure.walk/keywordize-keys
                          (get-in [:response :body :message])
                          clojure.string/capitalize)]
          (rf/dispatch [:subscription-error message]))))))
