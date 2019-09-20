<?php

    $json_file = file_get_contents('../scraped_data/arachnid_data.json');
    $scraped_data = json_decode($json_file, true);

    if (file_get_contents('../scraped_data/warnings.json')) {
        $warning_file = file_get_contents('../scraped_data/warnings.json');
        $warnings = json_decode($warning_file, true);

        foreach ($warnings as $warning) {
            $warning_url = $warning['url'];
            $warning_text = $warning['warning'];

            array_push($all_warnings, array($warning_url, $warning_text));
        }
    }

    ///////////////////////
    // PAGES & DOMAINS & STRING OCCURANCE
    //////////////////////
    $site_title = $scraped_data['sites'][0]['netloc']; // Get site URL
    $pages  = array(); // Page URLs and their titles
    $full_url_pages = array();
    $domains     = array(); // Domains
    $custom_string_occurance  = array(); // Page URLs + the num of times the string occured
    $interesting_pages = array();
    $found_docs = array();
    for ($i = 0; $i < count($scraped_data['sites']); $i++) {
        // Find all page paths
        foreach ($scraped_data['sites'][$i]['pages'] as $page) {
                // Build the full url page arrary
                $full_url = "http://" . $scraped_data['sites'][$i]['netloc'] . $page['path'];
                // Build the general array that contains all pages + their title
                array_push($pages, array($full_url, $page['path'], $page['title']));



                // If any of the string occured on this page, append it to the seperate array of string occurances
                if ($page['custom_string_occurances'] > 0){
                    array_push($custom_string_occurance, array($page['path'], $page['custom_string_occurances']));
                }

                // If it's an interesting page, append it to the array
                if ($page['on_fuzz_list'] == True) {
                    array_push($interesting_pages, $full_url);
                }
            }

        // Find all docs in a given subdomain

        foreach ($scraped_data['sites'][$i]['documents'] as $document) {
            $full_document_url = "http://" . $scraped_data['sites'][$i]['netloc'] . $document['path'];
            array_push($found_docs, array($document['name'], $full_document_url));
        }

        // Find all domains and append them to array
        array_push($domains, $scraped_data['sites'][$i]['netloc']);
    }

    ///////////////////////
    // PHONE NUMBERS
    ///////////////////////
    $phone_numbers = array(); // All emails as a simple list
    foreach ($scraped_data['phone_numbers'] as $number) {
        array_push($phone_numbers, $number);
    }

    ///////////////////////
    // EMAILS
    ///////////////////////
    $emails = array(); // All emails as a simple list
    foreach ($scraped_data['emails'] as $email) {
        array_push($emails, $email);
    }

    ///////////////////////
    // SOCIAL LINKS
    ///////////////////////
    $social_links = array(); // All social handels + their domain
    foreach ($scraped_data['social_media'] as $social_link) {
        array_push($social_links, array($social_link['link'], $social_link['domain']));
    }

    ///////////////////////
    // CUSTOM REGEX
    ///////////////////////
    $custom_regex = array();
    foreach ($scraped_data['custom_regex'] as $regex) {
        array_push($custom_regex, $regex);
    }

    ///////////////////////
    // SCAN METADATA
    ///////////////////////

    // // TODO: Store these are an object

    // $start_time = $scraped_data["metadata"]["start_time"];
    // $end_time = $scraped_data["metadata"]["end_time"];
    // $start_date = $scraped_data["metadata"]["start_date"];
    // $end_date = $scraped_data["metadata"]["end_date"];
    // $run_time = $scraped_data["metadata"]["run_time"];
    //
    // $sracpe_links = $scraped_data["metadata"]["config"]['scrape_links'];
    // $scrape_subdomains = $scraped_data["metadata"]["config"]['scrape_subdomains'];
    // $scrape_phone_number = $scraped_data["metadata"]["config"]['scrape_phone_number'];
    // $scrape_email = $scraped_data["metadata"]["config"]['scrape_email'];
    // $scrape_social_media = $scraped_data["metadata"]["config"]['scrape_social_media'];
    // $scraped_documents = $scraped_data["metadata"]["config"]['documents'];
    // $obey_robots = $scraped_data["metadata"]["config"]['obey_robots'];
    // $allow_query = $scraped_data["metadata"]["config"]['allow_query'];
    // $user_agent = $scraped_data["metadata"]["config"]['agent'];
    // $scraped_string = $scraped_data["metadata"]["config"]['custom_str'];
    // $scraped_strin_case_sensitive = $scraped_data["metadata"]["config"]['custom_str_case_sensitive'];
    // $custom_regex = $scraped_data["metadata"]["config"]['custom_regex'];
    // $default_delay = $scraped_data["metadata"]["config"]['default_delay'];
    // $page_fuzz_list = $scraped_data["metadata"]["config"]['paths_list_file_loc'];
    // $subdomain_fuzz_list = $scraped_data["metadata"]["config"]['subs_list_file_loc'];
    // $fuzz_paths = $scraped_data["metadata"]["config"]['fuzz_paths'];
    // $fuzz_subdomains = $scraped_data["metadata"]["config"]['fuzz_subs'];

    ////////////////////
    /// WARNINGS
    ///////////////////














 ?>
