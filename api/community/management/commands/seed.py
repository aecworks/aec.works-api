from django.core.management.base import BaseCommand
from django.utils.text import slugify

from api.community import factories as f
from api.community import models, services
from api.images.services import create_image_asset, create_image_file_from_url
from api.users.factories import ProfileFactory


class Command(BaseCommand):
    help = "Seed"

    def handle(self, *args, **options):
        profile = ProfileFactory()
        profile_2 = ProfileFactory()
        file = create_image_file_from_url(
            "https://upload.wikimedia.org/wikipedia/commons/4/49/Mosuo_Woman_-_42723465920.jpg"
        )
        profile.avatar = create_image_asset(img_file=file)
        profile.save()

        for (
            name,
            description,
            website,
            location,
            logo_url,
            cover_url,
            hashtag_names,
        ) in seed_data:

            slug = slugify(name)
            company = models.Company.objects.filter(slug=slug).first()
            if company:
                print(f"> Already exists: {slug} - flush or delete to recreate")
                continue
            else:
                print(f"> Created: {slug}")
                hashtags = services.get_or_create_hashtags(hashtag_names)
                attrs = services.CompanyRevisionAttributes(
                    name=name,
                    description=description,
                    website=website,
                    location=location,
                    twitter="aec_works",
                    crunchbase_id="apple",
                    logo=None,
                    cover=None,
                    hashtags=hashtags,
                )
                company = services.create_company(created_by=profile, attrs=attrs)

            # Logo
            logo_file = create_image_file_from_url(logo_url)
            logo_img = create_image_asset(img_file=logo_file)
            company.current_revision.logo = logo_img

            # Cover
            cover_file = create_image_file_from_url(cover_url)
            cover_img = create_image_asset(img_file=cover_file)
            company.current_revision.cover = cover_img

            company.current_revision.save()
            print(f"    logo: {logo_url}")
            print(f"    cover: {cover_url}")

            comments = [
                f.CommentFactory(profile=profile, thread=company.thread)
                for _ in range(3)
            ]

            services.comment_clap(comment=comments[0], profile=profile)
            services.comment_clap(comment=comments[2], profile=profile_2)

            if name[0] > "g":
                services.company_clap(company=company, profile=profile)

            print("    comments")

            if name == "1Build" and company.articles.count() == 0:
                company.banner = "Hiring"
                company.save()
                services.create_company_article(
                    company=company,
                    url="https://www.archdaily.com/793082/la-serena-house-sebastian-gaviria-gomez?ad_medium=widget&ad_name=selected-buildings-stream",
                    profile=profile,
                )
                services.create_company_article(
                    company=company,
                    url="https://www.archdaily.com/788489/nilo-houses-alberto-burckhard-plus-carolina-echeverri?ad_medium=widget&ad_name=recommendation",
                    profile=profile,
                )


# [(c.name,c.description, c.logo.file.url, c.cover.file.url, [h.slug for h in c.hashtags.all()]) for c in C.objects.all() if c.logo and c.cover][:30]
seed_data = [
    (
        "Morpholio",
        "Morpholio, a group of applications that reinvent creative processes for designers, artists, photographers and any imaginative individual.",
        "https://www.morpholioapps.com/",
        "New York City, NY, USA",
        "https://static.aec.works/images/05baf21e4d564ff4ac9b31e416555ba6.png",
        "https://static.aec.works/images/0d878f475ad6422190efc1cb84c4b08b.png",
        ["Sketching", "Software"],
    ),
    (
        "Outfit Renovations",
        "Renovations made by you - materials, tools, and instructions delivered to your door for your next DIY renovation",
        "https://www.outfitrenovations.com/",
        "San Francisco, United States",
        "https://static.aec.works/images/e1fd8a6de1624788b10b8e655f0932aa.png",
        "https://static.aec.works/images/b945c68ec31846a3a46b8e843b3a9980.png",
        ["Remodeling"],
    ),
    (
        "UrbanForm",
        "UrbanForm is an online resource for zoning regulations that calculates what can be built on a piece of land. Complex zoning that used to take hours or even weeks to calculate is now available instantaneously.",
        "https://urbanform.us",
        "Portland, United States",
        "https://static.aec.works/images/b6d409048cd64942b47c32661a69f85d.png",
        "https://static.aec.works/images/ebccdd1e41d5452897e2038eb454fcec.png",
        ["Regulatory", "UrbanDesign", "LandUse"],
    ),
    (
        "aec.works",
        "aec.works is an open source website that offers a curated list of kick-ass product-oriented AEC companies and startups. \n\nFormerly AecStartups.com",
        "https://aec.works",
        "San Francisco, United States",
        "https://static.aec.works/images/083a4e1e8daf446497a4e40831299557.png",
        "https://static.aec.works/images/03659d8dfd524d9abf6a8d337476f216.png",
        [],
    ),
    (
        "1Build",
        "On-demand cost estimating service for builders. We create accurate takeoffs and estimates to help contractors win more bids.",
        "https://www.1build.com",
        "San Francisco, United States",
        "https://static.aec.works/images/b3c7208c9bac45c8ac9809762ac80a8c.png",
        "https://static.aec.works/images/359989bc6d664a4da43b872827f63807.png",
        ["CostEstimation"],
    ),
    (
        "Mosaic",
        "Mosaic is a construction technology company that provides adaptive solutions for planning and construction in the homebuilding industry. \n\nWe enable teams to build beautiful and unique homes faster and more efficiently than anyone else, anywhere",
        "https://mosaic.us",
        "Phoenix, AZ, USA",
        "https://static.aec.works/images/a277b142d9024a7390538a901be10f76.png",
        "https://static.aec.works/images/04de99abb1284eafb5747a1411c04e0c.png",
        ["ConstructionTechnology"],
    ),
    (
        "Renga",
        "Architectural 3D BIM (CAD) for Design and Construction",
        "https://rengabim.com/en/",
        "Saint-Petersburg, Russia",
        "https://static.aec.works/images/4f446ce08a134c6b96427b871ac251f6.png",
        "https://static.aec.works/images/7baf400e7503404998be31469cd34fb3.png",
        ["Modeling", "Bim"],
    ),
    (
        "New Frontier Tiny Homes",
        "Prefabricated homes for every lifestyle",
        "https://www.newfrontiertinyhomes.com",
        "Nashville, USA",
        "https://static.aec.works/images/521018fb9ec24fde9ef43a090afa4594.png",
        "https://static.aec.works/images/d024f583c0724447b2e4c2f4d9357261.png",
        ["Prefab", "Housing", "Adu"],
    ),
    (
        "Dwellito",
        "Dwellito is a modular home marketplace that helps you find, compare, and purchase a prefab modular home",
        "https://www.dwellito.com/",
        "Unknown",
        "https://static.aec.works/images/363f53b05eb3482299670e3f52866ea4.png",
        "https://static.aec.works/images/8f8b27d3c9c14793ba03fabc677f8589.png",
        ["Prefab", "Housing", "Adu"],
    ),
    (
        "Cityzenith",
        "Cityzenith builds advanced Digital Twin software solutions for buildings, infrastructure, and smart cities.",
        "https://cityzenith.com/",
        "Chicago, IL, USA",
        "https://static.aec.works/images/a615b489d2de499caa8fc619f902eafc.png",
        "https://static.aec.works/images/831623e9302846b3a64c82e810f64a91.png",
        ["UrbanDesign", "Bim", "DigitalTwin"],
    ),
    (
        "Mighty Buildings",
        "Mighty Buildings is a prefab modular construction company working on disrupting the residential housing market.",
        "https://www.mightybuildings.com",
        "San Francisco, CA, USA",
        "https://static.aec.works/images/d974b126c3334936b980603ff9ab168b.png",
        "https://static.aec.works/images/83e87eca335246d9980a667b56ee2622.png",
        ["Prefab", "Housing", "Adu"],
    ),
    (
        "Monograph",
        "Project Management Software For Architects & Engineers",
        "https://monograph.io",
        "San Francisco, CA, USA",
        "https://static.aec.works/images/b68c3c970007498fb79fd4edff5ef407.png",
        "https://static.aec.works/images/e6f1f5d80ee74875a2b1fce89b26d100.png",
        ["ProjectManagement"],
    ),
    (
        "Apt",
        "Apt is a Natively Integrated Developer aiming to create a nationwide housing development chain by standardizing its products on a building level.",
        "https://apt.re",
        "Los Angeles, United States",
        "https://static.aec.works/images/0e026cf139ce43209bc348911741a234.png",
        "https://static.aec.works/images/c1256e05e18f41159679a86fe5b050d4.png",
        ["Housing"],
    ),
    (
        "Hypar",
        "We provide a cloud compute environment and software libraries that enable AEC developers to deploy their specialized building logic to the cloud, and make it available to their team, their organization, or the world.",
        "https://hypar.io/",
        "Culver City, CA, USA",
        "https://static.aec.works/images/0bf94a3529be4e7ebc96496478b7fe44.png",
        "https://static.aec.works/images/863ef7e98a294f62b73e4b8d19761dec.png",
        ["Interoperability", "Generative", "DesignAutomation"],
    ),
    (
        "Plant Prefab",
        "We design and build custom, high-quality, sustainable homes, based on your designs or ours.",
        "https://www.plantprefab.com",
        "Rialto, CA, USA",
        "https://static.aec.works/images/e84f684a9b114c1d9eb9d428f6eb98f1.png",
        "https://static.aec.works/images/12e89b127aa34b62b9e20c6fa407597d.png",
        ["Prefab", "Housing", "Adu"],
    ),
    (
        "ProTenders",
        "Where the Construction Industry Connects, Sources & Procures",
        "https://www.protenders.com/",
        "UAE",
        "https://static.aec.works/images/147cc0f2555d44ea97e88bedc0ad66c9.png",
        "https://static.aec.works/images/df95dee06e1443569c7e218489583880.png",
        ["ConstructionManagement"],
    ),
    (
        "Rent TheBackyard",
        "Earn cash renting out an apartment in your backyard",
        "https://rentthebackyard.com/",
        "California, USA",
        "https://static.aec.works/images/53c70401b25f49668678d62903d89758.png",
        "https://static.aec.works/images/5ac0ebd494f24d10bd10c157ca1f929b.png",
        ["Housing", "Adu"],
    ),
    (
        "Saltmine",
        "A cloud-based workplace design platform built for global enterprises",
        "https://www.saltmine.com",
        "San Francisco, CA USA",
        "https://static.aec.works/images/c17f23a24a614f72b5c35431c617f8b8.png",
        "https://static.aec.works/images/624945f49f7a4c7e81fa2e86cca84223.png",
        ["Workplace", "DataManagement"],
    ),
    (
        "Samara | Backyard",
        "An initiative to prototype new ways that homes can be built and shared, guided by an ambition to realize more humanistic, future-oriented, and waste-conscious design.",
        "https://samara.com/backyard/",
        "San Francisco, CA, USA",
        "https://static.aec.works/images/ea267e1e2f6149b08bc47625f0e45999.png",
        "https://static.aec.works/images/b3e5662c22dd4e138c10596143c751fe.png",
        ["Housing"],
    ),
    (
        "Scaled Robotics",
        "Robotic Constrution",
        "https://www.scaledrobotics.com/",
        "Barcelona, Spain",
        "https://static.aec.works/images/1f94eef1dbc44724976e6dc436b4f3ce.png",
        "https://static.aec.works/images/b5ec6761c485490bb5797aa01b263cb1.png",
        ["ConstructionTechnology", "Robotics"],
    ),
    (
        "Skipp",
        "Kitchen Renovations Made Simple",
        "https://skipp.co/",
        "New York, NY, USA",
        "https://static.aec.works/images/ae32030229d64321b7a8135dc8e369d6.png",
        "https://static.aec.works/images/6907ed84c7e24ba7bfda0e6aeefd6bf6.png",
        ["Remodeling"],
    ),
    (
        "Floored",
        "Interactive real estate marketing and leasing tool that puts real estate professionals in control of their test-fits. Acquired by CBRE.",
        "https://www.floored.com/",
        "Somewhere",
        "https://static.aec.works/images/00f4afa01c5844c1a2eeefe07ebd72eb.png",
        "https://static.aec.works/images/431276786b004d9893df6a5cb6f0e843.png",
        ["DesignAutomation", "SpacePlanning"],
    ),
    (
        "Spacemaker",
        "The site intelligence platform for early-stage real-estate development that combines cloud computing and AI",
        "https://spacemaker.ai",
        "Oslo, Norway",
        "https://static.aec.works/images/9c6fb7c8bdb34268b6ef3b5ed2dfada3.png",
        "https://static.aec.works/images/95985d64d0574753a1638420e9f93c70.png",
        ["UrbanDesign"],
    ),
    (
        "SpecifiedBy",
        "Construction product research database",
        "https://www.specifiedby.com",
        "UK",
        "https://static.aec.works/images/53aaddeda3074bb9b5da9cb79da533d4.png",
        "https://static.aec.works/images/b6113f0611be4e8fa224f4c9c75e4a05.png",
        ["SupplyChain", "ConstructionManagement"],
    ),
    (
        "StructionSite",
        "A site capture combining 360 cameras and AI for construction progress tracking",
        "https://www.structionsite.com",
        "Oakland, CA, USA",
        "https://static.aec.works/images/518934b90fb047ada6d77d365fbecf3b.png",
        "https://static.aec.works/images/d1b3c53999b4456d845e579d3f92a693.png",
        ["ConstructionManagement", "IssueTracking"],
    ),
    (
        "Room",
        "Soundproof office phone booths and meeting pods.",
        "https://room.com",
        "New York, NY, USA",
        "https://static.aec.works/images/d5d334db6473497dbb3eb1f6565d1072.png",
        "https://static.aec.works/images/817975be80c04ed9bc8f8b643fecbf3d.png",
        ["Prefab", "InteriorDesign", "Furniture"],
    ),
    (
        "United Dwellings",
        "United Dwelling partners with homeowners to transform underutilized garages and backyards into affordable, high-quality homes known as Accessory Dwelling Units",
        "https://www.uniteddwelling.com/",
        "Culver City, United States",
        "https://static.aec.works/images/136a442a90b04eac808d09ae52733dd2.png",
        "https://static.aec.works/images/8966242eada04b02b25ead790f6cb173.png",
        ["Remodeling", "Adu"],
    ),
    (
        "Replica",
        "Replica is a next-generation urban planning tool that can help cities answer key transportation questions.",
        "https://replicahq.com/",
        "San Francisco, CA, USA",
        "https://static.aec.works/images/f28e6af922d84fd094aac919fdc1d92b.png",
        "https://static.aec.works/images/338b993247c54271a2d3f6314ca84665.png",
        ["Transportation", "UrbanDesign"],
    ),
    (
        "Briq",
        "Briq is a corporate performance management platform built to make the lives of construction financial professionals easier, and to make contractors more profitable.",
        "https://br.iq/",
        "Santa Barbara, United States",
        "https://static.aec.works/images/111aa5faa0b845438b9ac6edd82c3fc8.png",
        "https://static.aec.works/images/1b30b70bd34b4c3f8aa5cc73bdc328a6.png",
        ["Finance", "ConstructionManagement"],
    ),
    (
        "UpCodes",
        "UpCodes helps the AEC industry deliver code compliant buildings.",
        "https://up.codes/",
        "San Francisco, CA, USA",
        "https://static.aec.works/images/9c676e25a83a4b149a4d715ada37b5ea.png",
        "https://static.aec.works/images/9657fcbf7268470382b099ab26712936.png",
        ["CodeCompliance"],
    ),
]
