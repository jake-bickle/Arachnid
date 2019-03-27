<?php

    $json_file = file_get_contents('../scraped_data/arachnid_data.json');
    $scraped_data = json_decode($json_file, true);

    ///////////////////////
    // PAGES & DOMAINS & STRING OCCURANCE
    //////////////////////zx
    $pages  = array(); // Page URLs and their titles
    $full_url_pages = array();
    $domains     = array(); // Domains
    $custom_string_occurance  = array(); // Page URLs + the num of times the string occured
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


 ?>
