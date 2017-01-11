public with sharing class ringBell {

    private static final string ENDPOINT = 'https://[yourendpoint].dataplicity.io/ring/{FAST | MEDIUM | SLOW }/{times}';
    private static Ring_My_Bell__c rmb;
    public string speed {get;set;}
    public string times {get;set;}
    
    public ringBell(){
        times = '1';
    }

    public PageReference submit(){
        string ipAddress = ApexPages.currentPage().getHeaders().get('X-Salesforce-SIP');
        
        rmb = new Ring_My_Bell__c();
        rmb.IP_Address__c = ipAddress;
        DateTime oneHourAgo = System.now().addHours(-1);
        
        system.debug('Last hour: ' + oneHourAgo);
        system.debug('IP Address: ' + ipAddress);
        
        List<Ring_My_Bell__c> existingIP = new List<Ring_My_Bell__c>([SELECT Id
                                                                      FROM Ring_My_Bell__c
                                                                      WHERE IP_Address__c =:ipAddress AND
                                                                            CreatedDate > :oneHourAgo]);
        if(existingIP.isEmpty()){
        
            try{
                ring(speed, times);
            } catch (Exception e){
                system.debug('There was an error: ' + e);
            }
        }
        
        return null;
    }


    @future (callout=true)
    public static void ring(String speed, String times) {

        HttpRequest req = new HttpRequest();
        HttpResponse res = new HttpResponse();
        Http http = new Http();

        req.setEndpoint(ENDPOINT);
        req.setMethod('POST');
        req.setBody('speed='+EncodingUtil.urlEncode(speed, 'UTF-8')+'&times='+EncodingUtil.urlEncode(times, 'UTF-8'));

        try {
            res = http.send(req);
        } catch(System.CalloutException e) {
            System.debug('Callout error: '+ e);
            System.debug(res.toString());
        }

    }
    
}
